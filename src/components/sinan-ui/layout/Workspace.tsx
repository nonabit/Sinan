import type { PropsWithChildren } from 'react'

export function Workspace({ children }: PropsWithChildren) {
  return <div className="workspace">{children}</div>
}
