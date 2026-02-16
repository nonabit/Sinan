// src/components/ScreenshotNode/index.tsx
interface ScreenshotNodeProps {
  stepId: number
  action: string
  targetDesc: string
  screenshot?: string
  status: 'pending' | 'running' | 'passed' | 'failed'
}

export function ScreenshotNode({
  stepId,
  action,
  targetDesc,
  screenshot,
  status,
}: ScreenshotNodeProps) {
  const statusLabel = {
    pending: 'Pending',
    running: 'Running',
    passed: 'Passed',
    failed: 'Failed',
  }[status]

  return (
    <div className={`step-card ${screenshot ? 'compact' : ''}`}>
      <div className="step-card-header">
        <span className="step-title">{action}</span>
        <span className={`step-badge ${status}`}>{statusLabel}</span>
      </div>
      {screenshot ? (
        <div className="screenshot-card">
          <div className="screenshot-preview">
            {screenshot ? (
              <img
                src={`data:image/png;base64,${screenshot}`}
                alt={`步骤 ${stepId}`}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="screenshot-placeholder">等待截图</div>
            )}
          </div>
          <div className="step-meta">
            步骤 {stepId} · {targetDesc}
          </div>
        </div>
      ) : (
        <div className="step-meta">
          步骤 {stepId} · {targetDesc}
        </div>
      )}
    </div>
  )
}
