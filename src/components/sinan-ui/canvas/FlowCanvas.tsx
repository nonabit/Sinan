import type { Node, Edge, Connection, OnNodesChange, OnEdgesChange, NodeTypes, EdgeTypes } from 'reactflow'
import ReactFlow, { Background, Controls, Panel } from 'reactflow'

interface FlowCanvasProps {
  nodes: Node[]
  edges: Edge[]
  onNodesChange: OnNodesChange
  onEdgesChange: OnEdgesChange
  onConnect: (connection: Connection) => void
  onLayout: () => void
  nodeTypes: NodeTypes
  edgeTypes: EdgeTypes
}

export function FlowCanvas({
  nodes,
  edges,
  onNodesChange,
  onEdgesChange,
  onConnect,
  onLayout,
  nodeTypes,
  edgeTypes,
}: FlowCanvasProps) {
  return (
    <section className="canvas-grid">
      <ReactFlow
        className="flow-canvas"
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={(connection) => onConnect(connection)}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        defaultEdgeOptions={{ type: 'dashed' }}
        connectionLineStyle={{
          stroke: 'var(--accent)',
          strokeWidth: 2,
          strokeDasharray: '7 8',
        }}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        proOptions={{ hideAttribution: true }}
      >
        <Background
          variant="dots"
          gap={26}
          size={1.6}
          color="rgba(120, 138, 175, 0.28)"
        />
        <Controls showInteractive={false} position="bottom-left" />
        <Panel position="top-right" className="canvas-actions">
          <button type="button" className="canvas-button" onClick={onLayout}>
            Auto Layout
          </button>
        </Panel>
      </ReactFlow>
    </section>
  )
}
