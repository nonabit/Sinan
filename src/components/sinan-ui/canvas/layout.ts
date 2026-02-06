import dagre from 'dagre'
import type { Node, Edge } from 'reactflow'

const FLOW_NODE_SIZE = { width: 220, height: 120 }
const DEVICE_NODE_SIZE = { width: 210, height: 230 }

const getNodeSize = (node: Node) => {
  if (node.type === 'device') return DEVICE_NODE_SIZE
  return FLOW_NODE_SIZE
}

export function layoutNodes<TNode extends Node, TEdge extends Edge>(
  nodes: TNode[],
  edges: TEdge[],
  direction: 'LR' | 'TB' = 'LR',
) {
  const dagreGraph = new dagre.graphlib.Graph()
  dagreGraph.setDefaultEdgeLabel(() => ({}))
  dagreGraph.setGraph({ rankdir: direction, nodesep: 90, ranksep: 140 })

  nodes.forEach((node) => {
    const { width, height } = getNodeSize(node)
    dagreGraph.setNode(node.id, { width, height })
  })

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target)
  })

  dagre.layout(dagreGraph)

  return nodes.map((node) => {
    const { width, height } = getNodeSize(node)
    const nodeWithPosition = dagreGraph.node(node.id) as { x: number; y: number }

    return {
      ...node,
      position: {
        x: nodeWithPosition.x - width / 2,
        y: nodeWithPosition.y - height / 2,
      },
    }
  })
}
