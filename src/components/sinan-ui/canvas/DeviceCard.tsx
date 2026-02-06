import type { CSSProperties } from 'react'

interface DeviceCardProps {
  footerText: string
  style?: CSSProperties
}

export function DeviceCard({ footerText, style }: DeviceCardProps) {
  return (
    <div className="device-card" style={style}>
      <div className="device-header">
        <div className="device-chip" />
        <div className="device-line" />
      </div>
      <div className="device-screen">
        <div className="device-pill-outline" />
        <div className="device-ring" />
        <div className="device-line short" />
      </div>
      <div className="device-footer">{footerText}</div>
    </div>
  )
}
