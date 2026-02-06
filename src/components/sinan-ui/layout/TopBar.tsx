import type { ReactNode } from 'react'

interface TopBarProps {
  deviceName: string
  deviceStatus: string
  title: string
  action?: ReactNode
}

export function TopBar({ deviceName, deviceStatus, title, action }: TopBarProps) {
  return (
    <header className="topbar">
      <div className="device-pill">
        <div className="device-dot" />
        <span className="device-name">{deviceName}</span>
        <span className="device-status">{deviceStatus}</span>
      </div>
      <div className="topbar-title">{title}</div>
      <div className="topbar-action">{action}</div>
    </header>
  )
}
