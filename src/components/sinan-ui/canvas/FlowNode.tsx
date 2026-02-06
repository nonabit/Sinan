import type { CSSProperties, ReactNode } from 'react'

type FlowStatus = 'success' | 'running'

interface FlowNodeProps {
  title: string
  status: FlowStatus
  bodyLines: ReactNode[]
  style?: CSSProperties
}

export function FlowNode({ title, status, bodyLines, style }: FlowNodeProps) {
  return (
    <div className="flow-node" style={style}>
      <div className="node-header">
        <span>{title}</span>
        <span className={`status-pill ${status}`}>
          {status === 'success' ? 'PASSED' : 'RUNNING'}
        </span>
      </div>
      <div className="node-body">
        {bodyLines.map((line, index) => (
          <div key={index}>{line}</div>
        ))}
      </div>
    </div>
  )
}
