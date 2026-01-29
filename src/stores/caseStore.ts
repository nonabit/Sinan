// src/stores/caseStore.ts
import { create } from 'zustand'

interface TestStep {
  stepId: number
  action: string
  targetDesc: string
  coordinates: number[]
  screenshot?: string
  status: 'pending' | 'running' | 'passed' | 'failed'
}

interface TestCase {
  caseId: string
  caseName: string
  steps: TestStep[]
  status: 'pending' | 'running' | 'passed' | 'failed'
}

interface CaseState {
  cases: TestCase[]
  currentCase: string | null
  addCase: (testCase: TestCase) => void
  updateStep: (caseId: string, stepId: number, update: Partial<TestStep>) => void
  setCurrentCase: (caseId: string) => void
}

export const useCaseStore = create<CaseState>((set) => ({
  cases: [],
  currentCase: null,
  addCase: (testCase) => set((state) => ({
    cases: [...state.cases, testCase]
  })),
  updateStep: (caseId, stepId, update) => set((state) => ({
    cases: state.cases.map(c =>
      c.caseId === caseId
        ? {
            ...c,
            steps: c.steps.map(s =>
              s.stepId === stepId ? { ...s, ...update } : s
            )
          }
        : c
    )
  })),
  setCurrentCase: (caseId) => set({ currentCase: caseId }),
}))
