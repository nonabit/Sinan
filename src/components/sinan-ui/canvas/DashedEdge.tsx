import type { EdgeProps } from 'reactflow'
import { BaseEdge, getBezierPath } from 'reactflow'

export function DashedEdge({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition }: EdgeProps) {
  const [edgePath] = getBezierPath({
    sourceX,
    sourceY,
    targetX,
    targetY,
    sourcePosition,
    targetPosition,
  })

  return <BaseEdge id={id} path={edgePath} className="dash-path" />
}
