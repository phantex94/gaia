// Compute-graph pane: /graph <board id | repo folder [--task name] | sample> draws graph.yaml with the task's slice.
import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { GraphEdge, GraphNode, Mode, View } from '../types'

const PANE = 'compute-graph'
const TITLE = 'Compute graph'
const REFRESH_MS = 5000
const WRITE_TOOLS = ['Edit', 'Write', 'MultiEdit', 'NotebookEdit', 'Bash']
const USAGE = 'Usage: /graph AMC-56 | /graph <repo folder> [--task name] | /graph sample | /graph (this folder)'
const MARK: Record<Mode, string> = { '': ' ', add: '+', rewire: '~', polish: '*', remove: 'x' }
const COLOR: Record<Mode, string | undefined> = {
  '': undefined,
  add: 'success',
  rewire: 'warning',
  polish: 'suggestion',
  remove: 'error',
}

const target = atom({ plugin: 'compute-graph', key: 'target' } as const, '')
const view = atom({ plugin: 'compute-graph', key: 'view' } as const, null as View | null, { shape: 'view-1' })

let cwd = ''

function argv(root: string, picked: string): string[] {
  const words = picked.split(/\s+/).filter(Boolean)
  const args = words[0] === 'sample' ? [`${root}/sample`, '--task', 'smp-1'] : words
  return [`${root}/scripts/compute_graph.py`, 'json', ...(args.length ? args : [cwd])]
}

async function fetchView($: EngineInterface, picked: string): Promise<View> {
  const script = argv($.plugin.root, picked)
  const runs = [['uv', 'run', '-q', '--script', ...script], ['python3', ...script]]
  let last = ''
  for (const run of runs) {
    try {
      const { exitCode, stdout, stderr } = await $.process.run(run, cwd ? { cwd } : undefined)
      if (stdout.trim().startsWith('{')) return JSON.parse(stdout) as View
      last = stderr.trim() || `exit ${exitCode}`
    } catch (error) {
      last = String(error)
    }
  }
  return { refusal: `Could not run compute_graph.py (needs uv, or python3 with PyYAML): ${last}` } as View
}

async function refresh($: EngineInterface): Promise<View> {
  const shown = await fetchView($, await read($, target))
  const now = await read($, view)
  if (JSON.stringify(now) !== JSON.stringify(shown)) await update($, view, () => shown)
  return shown
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const started = await next(e)
    cwd = e.cwd
    await $.command.register({ name: 'graph', description: 'Show a task\'s compute graph and slice in a pane' })
    $.clock.every(REFRESH_MS, () => {
      void (async () => {
        if ((await read($, view)) !== null) await refresh($)
      })()
    })
    return started
  })

  on('command.run', { command: 'graph' }, async ($, e) => {
    await update($, target, () => e.args.trim())
    const shown = await refresh($)
    await $.ui.open({ id: PANE, title: TITLE })
    if (shown.refusal) return { text: `${shown.refusal}\n${USAGE}` }
    const head = [shown.repo, shown.task].filter(Boolean).join(' · ')
    return { text: `${TITLE}: ${head}. ${[...shown.errors, ...shown.notes].join(' ') || 'Slice shown in the pane.'}` }
  })

  on('tool.call', async ($, e, next) => {
    const ran = await next(e)
    if (WRITE_TOOLS.includes(e.tool) && (await read($, view)) !== null) await refresh($)
    return ran
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const shown = await read($, view)
    if (shown === null) return <Text dimColor>{USAGE}</Text>
    if (shown.refusal) {
      return (
        <Box flexDirection="column">
          <Text color="error">{shown.refusal}</Text>
          <Text dimColor>{USAGE}</Text>
        </Box>
      )
    }
    const hasSlice = shown.slice === 'found'
    const outgoing = (node: GraphNode): GraphEdge[] => shown.edges.filter(edge => edge.from === node.id)
    const axis = (node: GraphNode) =>
      node.missing ? 'missing in graph.yaml' : `${node.axis.toUpperCase()}${node.group_by ? `(${node.group_by})` : ''}`
    const row = (node: GraphNode) => (
      <Box flexDirection="column">
        <Text color={COLOR[node.mode]} dimColor={hasSlice && !node.mode} weight={node.mode ? 'bold' : 'regular'}>
          {`${MARK[node.mode]} ${node.id}  ${axis(node)}`}
        </Text>
        {outgoing(node).map(edge => (
          <Text color={COLOR[edge.mode]} dimColor={!edge.mode}>
            {`    ${edge.mode === 'remove' ? '⇢' : '→'} ${edge.to}${edge.carries ? ` (${edge.carries})` : ''}`}
          </Text>
        ))}
      </Box>
    )
    const lanes = [...shown.stages, { id: '', title: 'Missing in graph.yaml' }]
    return (
      <Box flexDirection="column">
        <Text weight="bold">{[shown.repo, shown.task].filter(Boolean).join(' · ')}</Text>
        <Text dimColor>{`${shown.source} · ${shown.intent_file || 'no intent file'}`}</Text>
        {shown.errors.map(line => (
          <Text color="error">{line}</Text>
        ))}
        {shown.notes.map(line => (
          <Text color="warning">{line}</Text>
        ))}
        {hasSlice && <Text dimColor>+ add  ~ rewire  * polish  ⇢ removed edge</Text>}
        {lanes.map(lane => {
          const nodes = shown.nodes.filter(node => (lane.id ? node.stage === lane.id : node.missing))
          if (nodes.length === 0) return null
          return (
            <Box flexDirection="column" marginTop={1}>
              <Text dimColor weight="bold">{lane.title.toUpperCase()}</Text>
              {nodes.map(row)}
            </Box>
          )
        })}
        {shown.clis.length > 0 && (
          <Box flexDirection="column" marginTop={1}>
            <Text dimColor weight="bold">CLI ↔ SUB-PATH</Text>
            {shown.clis.map(cli => (
              <Text color={COLOR[cli.mode]} dimColor={hasSlice && !cli.mode}>
                {`${MARK[cli.mode]} ${cli.command}: ${cli.path.join(' → ')}`}
              </Text>
            ))}
          </Box>
        )}
      </Box>
    )
  })
}
