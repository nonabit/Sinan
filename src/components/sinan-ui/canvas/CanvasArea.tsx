import type { PropsWithChildren } from 'react'
import { FlowConnector } from './FlowConnector'

interface CanvasAreaProps extends PropsWithChildren {
  connectors?: string[]
  viewBox?: string
}

export function CanvasArea({ connectors = [], viewBox = '0 0 1200 760', children }: CanvasAreaProps) {
  return (
    <section className="canvas-grid">
      <svg className="canvas-connector" viewBox={viewBox} preserveAspectRatio="none">
        {connectors.map((path, index) => (
          <FlowConnector key={`${path}-${index}`} d={path} />
        ))}
      </svg>
      {children}
    </section>
  )
}
