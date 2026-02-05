// src/App.tsx
import { ChatPanel } from './components/ChatPanel'
import { DeviceSelector } from './components/DeviceSelector'
import { ScreenshotNode } from './components/ScreenshotNode'
import { useCaseStore } from './stores/caseStore'
import { useDeviceMonitor } from './hooks/useDeviceMonitor'
import './App.css'

function App() {
  const { cases, currentCase } = useCaseStore()
  const activeCase = cases.find((c) => c.caseId === currentCase)

  // 启动设备监控
  useDeviceMonitor()

  return (
    <div className="h-screen flex bg-gray-50">
      {/* 左侧：画布区域 */}
      <div className="flex-1 p-4 overflow-auto">
        <h1 className="text-2xl font-bold mb-4">司南 (Sinan)</h1>

        {/* 用例执行画布 */}
        <div className="bg-white rounded-lg border p-4 min-h-[400px]">
          {activeCase ? (
            <div className="flex flex-wrap gap-4">
              {activeCase.steps.map((step) => (
                <ScreenshotNode
                  key={step.stepId}
                  stepId={step.stepId}
                  action={step.action}
                  targetDesc={step.targetDesc}
                  screenshot={step.screenshot}
                  status={step.status}
                />
              ))}
            </div>
          ) : (
            <div className="flex items-center justify-center h-full text-gray-400">
              <p>选择或创建测试用例开始</p>
            </div>
          )}
        </div>
      </div>

      {/* 右侧：控制面板 */}
      <div className="w-96 border-l bg-white flex flex-col">
        <DeviceSelector />
        <div className="flex-1">
          <ChatPanel />
        </div>
      </div>
    </div>
  )
}

export default App
