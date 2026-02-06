type PlanStatus = 'success' | 'running'

interface PlanStepProps {
  status: PlanStatus
  title: string
  subtitle: string
}

export function PlanStep({ status, title, subtitle }: PlanStepProps) {
  return (
    <div className={`plan-step ${status}`}>
      <div className="step-icon">
        <span />
      </div>
      <div className="step-text">
        <div className="step-title">{title}</div>
        <div className="step-subtitle">{subtitle}</div>
      </div>
    </div>
  )
}
