// src/App.tsx
import { Download } from 'lucide-react'
import { ChatPanel } from './components/ChatPanel'
import { DeviceSelector } from './components/DeviceSelector'
import { FlowCanvas } from './components/FlowCanvas'
import { Button } from './components/ui'
import { useCaseStore } from './stores/caseStore'
import { useDeviceMonitor } from './hooks/useDeviceMonitor'
import './App.css'

function App() {
  const { cases, currentCase } = useCaseStore()
  const activeCase = cases.find((c) => c.caseId === currentCase)
  const hasRealSteps = Boolean(activeCase && activeCase.steps.length > 0)
  const mockSteps = [
    {
      stepId: 1,
      action: 'Start Session',
      targetDesc: 'Initialize Android environment · Load config: Prod_Env_A',
      screenshot:
        'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==',
      status: 'passed' as const,
    },
    {
      stepId: 2,
      action: 'Tap Login',
      targetDesc: 'Tap "Login"',
      screenshot:
        'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==',
      status: 'passed' as const,
    },
    {
      stepId: 3,
      action: 'Verify Dashboard',
      targetDesc: 'Check element visibility · #dashboard_root',
      status: 'running' as const,
    },
  ]
  const stepsToRender = hasRealSteps
    ? activeCase!.steps.map((step) => ({
        stepId: step.stepId,
        action: step.action,
        targetDesc: step.targetDesc,
        screenshot: step.screenshot,
        status: step.status,
      }))
    : mockSteps

  // 启动设备监控
  useDeviceMonitor()

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-header-left">
          <DeviceSelector />
        </div>
        <div className="app-title">
          Sinan Automated Testing / <span>Checkout Flow v2.4</span>
        </div>
        <Button className="ui-export-btn" variant="primary" size="sm">
          <Download size={16} />
          Export Report
        </Button>
      </header>

      <div className="app-body">
        <main className="app-canvas">
          {stepsToRender.length > 0 ? (
            <FlowCanvas
              steps={stepsToRender}
              showDemoNote={!hasRealSteps}
            />
          ) : (
            <div className="canvas-empty">
              <p>选择或创建测试用例开始</p>
            </div>
          )}
        </main>

        <aside className="app-aside">
          <ChatPanel />
        </aside>
      </div>
    </div>
  )
}

export default App
