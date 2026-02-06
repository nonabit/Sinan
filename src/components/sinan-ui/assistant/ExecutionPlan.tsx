import type { ReactNode } from 'react'
import { PlanStep } from './PlanStep'

type PlanStatus = 'success' | 'running'

interface ExecutionStep {
  id: string
  status: PlanStatus
  title: string
  subtitle: string
}

interface ExecutionPlanProps {
  summary: ReactNode
  steps: ExecutionStep[]
}

export function ExecutionPlan({ summary, steps }: ExecutionPlanProps) {
  return (
    <div className="plan-card">
      <p>{summary}</p>
      {steps.map((step) => (
        <PlanStep
          key={step.id}
          status={step.status}
          title={step.title}
          subtitle={step.subtitle}
        />
      ))}
    </div>
  )
}
