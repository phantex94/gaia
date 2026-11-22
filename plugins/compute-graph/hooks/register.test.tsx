import { expect, test } from 'claude-code/testing'

const PANE = {
  plugin: 'compute-graph',
  component: 'Pane',
  requestId: 'compute-graph',
  props: {
    title: 'Compute graph',
    isFocused: false,
    bodyColumns: 60,
    placement: 'dock',
    scroll: { offset: 0, bodyRows: 40 },
    view: {},
  },
} as const

const STAGES = [
  { id: 'data', title: 'Data' },
  { id: 'factor', title: 'Factor' },
  { id: 'model', title: 'Signal / Model' },
]

const SLICED = {
  repo: 'sample-cta',
  task: 'SMP-1',
  source: 'checkout /repo',
  graph_file: 'docs/intent/graph.yaml',
  intent_file: 'docs/intent/smp-1-carry-factor.yaml',
  slice: 'found',
  stages: STAGES,
  nodes: [
    { id: 'pit_bars', stage: 'data', axis: 'ts', mode: 'polish' },
    { id: 'momentum', stage: 'factor', axis: 'ts', mode: '' },
    { id: 'carry_factor', stage: 'factor', axis: 'ts', mode: 'add' },
    { id: 'alpha_blend', stage: 'model', axis: 'cs', group_by: 'trading_day', mode: 'rewire' },
    { id: 'vol_target', stage: '', axis: '', mode: 'add', missing: true },
  ],
  edges: [
    { from: 'pit_bars', to: 'carry_factor', mode: 'add' },
    { from: 'momentum', to: 'alpha_blend', mode: 'remove' },
  ],
  clis: [{ command: 'cta signal build', path: ['pit_bars', 'carry_factor', 'alpha_blend'], mode: 'rewire' }],
  errors: ["slice node 'vol_target' is missing in graph.yaml"],
  notes: [],
}

const NO_SLICE = {
  ...SLICED,
  task: 'AMC-56',
  intent_file: '',
  slice: 'none',
  nodes: SLICED.nodes.slice(0, 2).map(node => ({ ...node, mode: '' })),
  edges: [],
  clis: [],
  errors: [],
  notes: ['AMC-56: no graph slice (no intent file in docs/intent).'],
}

function engine(on: any, shown: object, seen: string[][]) {
  on('command.register', () => ({ value: { command: 'graph' } }))
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('session.start', (_: unknown, e: { cwd: string }) => ({ cwd: e.cwd }))
  on('process.run', (_: unknown, e: { argv: string[] }) => {
    seen.push(e.argv)
    return { value: { exitCode: 0, stdout: JSON.stringify(shown), stderr: '' } }
  })
}

test('the pane marks the slice: add, rewire, polish, removed edge, missing id', async ($, on) => {
  const seen: string[][] = []
  engine(on, SLICED, seen)
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  await $.command.run({ command: 'graph', args: 'sample' })
  expect(seen[0]?.join(' ')).toContain('--task smp-1')

  for (const surface of ['terminal', 'desktop'] as const) {
    const ui = await $.ui.mount({ ...PANE, surface })
    expect((await ui.find({ type: 'Text', text: /carry_factor  TS/ }))?.text).toBe('+ carry_factor  TS')
    expect((await ui.find({ type: 'Text', text: /alpha_blend  CS/ }))?.text).toBe('~ alpha_blend  CS(trading_day)')
    expect((await ui.find({ type: 'Text', text: /pit_bars  TS/ }))?.text).toBe('* pit_bars  TS')
    expect((await ui.find({ type: 'Text', text: /⇢ alpha_blend/ }))?.text).toBe('    ⇢ alpha_blend')
    expect((await ui.find({ type: 'Text', text: /\+ vol_target/ }))?.text).toBe('+ vol_target  missing in graph.yaml')
    expect((await ui.find({ type: 'Text', text: /cta signal build/ }))?.text).toContain('~ cta signal build')
    await ui.unmount()
  }
})

test('a task without an intent file shows the repo graph and says it has no slice', async ($, on) => {
  engine(on, NO_SLICE, [])
  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const { text } = (await $.command.run({ command: 'graph', args: 'AMC-56' })) as { text: string }
  expect(text).toContain('no graph slice')

  const ui = await $.ui.mount({ ...PANE, surface: 'terminal' })
  expect((await ui.find({ type: 'Text', text: /no graph slice/ }))?.text).toBe(NO_SLICE.notes[0])
  expect((await ui.find({ type: 'Text', text: /momentum/ }))?.text).toBe('  momentum  TS')
  await ui.unmount()
})

test('before /graph the pane says how to pick a task', async $ => {
  const ui = await $.ui.mount({ ...PANE, surface: 'terminal' })
  expect((await ui.find({ type: 'Text' }))?.text).toContain('Usage: /graph AMC-56')
  await ui.unmount()
})
