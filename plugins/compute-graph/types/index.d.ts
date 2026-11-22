export type Mode = '' | 'add' | 'rewire' | 'polish' | 'remove'

export type GraphNode = {
  id: string
  stage: string
  axis: string
  group_by?: string
  inputs?: string[]
  outputs?: string[]
  mode: Mode
  missing?: boolean
}

export type GraphEdge = { from: string; to: string; carries?: string; mode: Mode; missing?: boolean }

export type GraphCli = { command: string; path: string[]; mode: Mode; missing?: boolean }

export type View = {
  repo: string
  task: string
  source: string
  graph_file: string
  intent_file: string
  slice: 'found' | 'none' | 'ambiguous'
  stages: { id: string; title: string }[]
  nodes: GraphNode[]
  edges: GraphEdge[]
  clis: GraphCli[]
  errors: string[]
  notes: string[]
  refusal?: string
}

declare module 'claude-code' {
  interface PluginState {
    'compute-graph': { target: string; view: Shaped<View | null> }
  }
}
