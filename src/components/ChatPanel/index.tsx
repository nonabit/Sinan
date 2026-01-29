// src/components/ChatPanel/index.tsx
import { useState, useCallback } from 'react'
import { MessageList } from './MessageList'
import { InputBox } from './InputBox'
import { useWebSocket } from '../../hooks/useWebSocket'
import { useCaseStore } from '../../stores/caseStore'
import { useDeviceStore } from '../../stores/deviceStore'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const { updateStep } = useCaseStore()
  const { selectedDevice } = useDeviceStore()

  const handleWebSocketMessage = useCallback((msg: { type: string; payload?: Record<string, unknown> }) => {
    if (msg.type === 'step_start') {
      const { caseId, stepId } = msg.payload as { caseId: string; stepId: number }
      updateStep(caseId, stepId, { status: 'running' })
    } else if (msg.type === 'step_done') {
      const { caseId, stepId, screenshot } = msg.payload as { caseId: string; stepId: number; screenshot: string }
      updateStep(caseId, stepId, { status: 'passed', screenshot })
    } else if (msg.type === 'case_done') {
      setIsLoading(false)
      const result = (msg.payload as { result: string })?.result
      const aiMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: `用例执行完成！结果：${result}`,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, aiMessage])
    } else if (msg.type === 'error') {
      setIsLoading(false)
      const errorMsg = (msg.payload as { message: string })?.message
      const aiMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: `错误：${errorMsg}`,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, aiMessage])
    }
  }, [updateStep])

  const { connected, send } = useWebSocket({
    url: 'ws://localhost:8000/ws',
    onMessage: handleWebSocketMessage,
  })

  const handleSend = useCallback(async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    }
    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)

    // 发送执行命令
    if (content.startsWith('执行')) {
      send({ type: 'execute', payload: { instruction: content, device: selectedDevice } })
    } else {
      // 模拟 AI 响应
      setTimeout(() => {
        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: `收到指令：${content}\n正在分析...`,
          timestamp: new Date(),
        }
        setMessages((prev) => [...prev, aiMessage])
        setIsLoading(false)
      }, 1000)
    }
  }, [send, selectedDevice])

  return (
    <div className="flex h-full flex-col bg-white">
      <div className="border-b p-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold">AI 助手</h2>
        <span className={`text-xs ${connected ? 'text-green-500' : 'text-red-500'}`}>
          {connected ? '已连接' : '未连接'}
        </span>
      </div>
      <MessageList messages={messages} />
      <InputBox onSend={handleSend} disabled={isLoading || !connected} />
    </div>
  )
}
