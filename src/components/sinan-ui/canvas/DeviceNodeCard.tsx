import { Handle, Position, type NodeProps } from 'reactflow'
import { DeviceCard } from './DeviceCard'

export interface DeviceNodeData {
  footerText: string
}

export function DeviceNodeCard({ data }: NodeProps<DeviceNodeData>) {
  return (
    <div>
      <Handle type="target" position={Position.Left} />
      <DeviceCard footerText={data.footerText} />
      <Handle type="source" position={Position.Right} />
    </div>
  )
}
