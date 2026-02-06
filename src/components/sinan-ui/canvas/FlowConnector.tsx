interface FlowConnectorProps {
  d: string
}

export function FlowConnector({ d }: FlowConnectorProps) {
  return <path className="dash-path" d={d} fill="none" />
}
