// src/hooks/useWebSocket.ts
import { useEffect, useRef, useCallback, useState } from 'react'

interface WebSocketMessage {
  type: string
  payload?: Record<string, unknown>
}

interface UseWebSocketOptions {
  url: string
  onMessage?: (message: WebSocketMessage) => void
  reconnectInterval?: number
}

export function useWebSocket({ url, onMessage, reconnectInterval = 3000 }: UseWebSocketOptions) {
  const wsRef = useRef<WebSocket | null>(null)
  const [connected, setConnected] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(url)

      ws.onopen = () => {
        setConnected(true)
        setError(null)
      }

      ws.onclose = () => {
        setConnected(false)
        // 自动重连
        setTimeout(connect, reconnectInterval)
      }

      ws.onerror = () => {
        setError('WebSocket 连接错误')
      }

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data) as WebSocketMessage
          onMessage?.(message)
        } catch (e) {
          console.error('解析消息失败:', e)
        }
      }

      wsRef.current = ws
    } catch (e) {
      setError('无法创建 WebSocket 连接')
    }
  }, [url, onMessage, reconnectInterval])

  const send = useCallback((message: WebSocketMessage) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message))
    }
  }, [])

  const disconnect = useCallback(() => {
    wsRef.current?.close()
  }, [])

  useEffect(() => {
    connect()
    return () => {
      wsRef.current?.close()
    }
  }, [connect])

  return { connected, error, send, disconnect }
}
