import { useEffect, useMemo } from 'react'
import ReactFlow, {
  Background,
  Controls,
  useEdgesState,
  useNodesState,
  type Edge,
  type Node,
} from 'reactflow'
import dagre from 'dagre'
import { ScreenshotNode } from '../ScreenshotNode'
import 'reactflow/dist/style.css'

type Step = {
  stepId: number
  action: string
  targetDesc: string
  screenshot?: string
  status: 'pending' | 'running' | 'passed' | 'failed'
}

const nodeWidth = 240
const nodeHeight = 260

function StepNode({ data }: { data: Step }) {
  return (
    <div className="flow-node">
      <ScreenshotNode
        stepId={data.stepId}
        action={data.action}
        targetDesc={data.targetDesc}
        screenshot={data.screenshot}
        status={data.status}
      />
    </div>
  )
}

const nodeTypes = { step: StepNode }

function buildGraph(steps: Step[]) {
  const nodes: Node<Step>[] = steps.map((step, index) => ({
    id: String(step.stepId),
    type: 'step',
    data: step,
    position: { x: index * (nodeWidth + 80), y: 0 },
    style: { width: nodeWidth, height: nodeHeight },
  }))

  const edges: Edge[] = steps.slice(0, -1).map((step, index) => ({
    id: `e${step.stepId}-${steps[index + 1].stepId}`,
    source: String(step.stepId),
    target: String(steps[index + 1].stepId),
    type: 'smoothstep',
    animated: true,
    style: {
      stroke: '#6366f1',
      strokeWidth: 2,
      strokeDasharray: '6 6',
    },
  }))

  return { nodes, edges }
}

function layoutGraph(nodes: Node[], edges: Edge[], direction: 'LR' | 'TB' = 'LR') {
  const dagreGraph = new dagre.graphlib.Graph()
  dagreGraph.setDefaultEdgeLabel(() => ({}))
  dagreGraph.setGraph({ rankdir: direction, nodesep: 40, ranksep: 60 })

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight })
  })
  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target)
  })

  dagre.layout(dagreGraph)

  const layoutedNodes = nodes.map((node) => {
    const { x, y } = dagreGraph.node(node.id)
    return {
      ...node,
      position: { x: x - nodeWidth / 2, y: y - nodeHeight / 2 },
    }
  })

  return { nodes: layoutedNodes, edges }
}

interface FlowCanvasProps {
  steps: Step[]
  showDemoNote?: boolean
}

export function FlowCanvas({ steps, showDemoNote }: FlowCanvasProps) {
  const initial = useMemo(() => buildGraph(steps), [steps])
  const [nodes, setNodes, onNodesChange] = useNodesState(initial.nodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(initial.edges)

  useEffect(() => {
    const { nodes: layoutedNodes, edges: layoutedEdges } = layoutGraph(
      initial.nodes,
      initial.edges,
      'LR',
    )
    setNodes(layoutedNodes)
    setEdges(layoutedEdges)
  }, [initial.nodes, initial.edges, setEdges, setNodes])

  return (
    <div className="flow-wrapper">
      {showDemoNote && (
        <div className="canvas-demo-note">
          Demo layout · connect a device or run a case to see live steps
        </div>
      )}
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodeTypes={nodeTypes}
        fitView
        nodesDraggable
        panOnScroll
        zoomOnScroll
      >
        <Background gap={24} size={1} color="#E2E8F0" />
        <Controls />
      </ReactFlow>
    </div>
  )
}
