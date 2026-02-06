import type { ReactNode } from 'react'
import { Handle, Position, type NodeProps } from 'reactflow'
import { FlowNode } from './FlowNode'

type FlowStatus = 'success' | 'running'

export interface FlowNodeData {
  title: string
  status: FlowStatus
  bodyLines: ReactNode[]
}

export function FlowNodeCard({ data }: NodeProps<FlowNodeData>) {
  return (
    <div>
      <Handle type="target" position={Position.Left} />
      <FlowNode title={data.title} status={data.status} bodyLines={data.bodyLines} />
      <Handle type="source" position={Position.Right} />
    </div>
  )
}
