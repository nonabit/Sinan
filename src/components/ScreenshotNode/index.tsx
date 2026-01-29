// src/components/ScreenshotNode/index.tsx
import { CheckCircle, XCircle, Loader } from 'lucide-react'

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
  const statusIcon = {
    pending: null,
    running: <Loader className="animate-spin text-blue-500" size={16} />,
    passed: <CheckCircle className="text-green-500" size={16} />,
    failed: <XCircle className="text-red-500" size={16} />,
  }

  return (
    <div className="w-48 rounded-lg border bg-white shadow-sm overflow-hidden">
      {/* 截图区域 */}
      <div className="h-32 bg-gray-100 flex items-center justify-center">
        {screenshot ? (
          <img
            src={`data:image/png;base64,${screenshot}`}
            alt={`步骤 ${stepId}`}
            className="w-full h-full object-cover"
          />
        ) : (
          <span className="text-gray-400 text-sm">等待截图</span>
        )}
      </div>

      {/* 信息区域 */}
      <div className="p-2">
        <div className="flex items-center justify-between">
          <span className="text-xs font-medium text-gray-500">
            步骤 {stepId}
          </span>
          {statusIcon[status]}
        </div>
        <p className="text-sm font-medium truncate" title={targetDesc}>
          {action}: {targetDesc}
        </p>
      </div>
    </div>
  )
}
