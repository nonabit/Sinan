import type { PropsWithChildren, ReactNode } from 'react'

interface AssistantPanelProps extends PropsWithChildren {
  title: string
  icon?: ReactNode
  footer?: ReactNode
}

export function AssistantPanel({ title, icon, footer, children }: AssistantPanelProps) {
  return (
    <aside className="assistant-panel">
      <div className="panel-header">
        {icon ? <span className="sparkle">{icon}</span> : null}
        {title}
      </div>
      <div className="panel-body">{children}</div>
      {footer ? <div className="panel-footer">{footer}</div> : null}
    </aside>
  )
}
