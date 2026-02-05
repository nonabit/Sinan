// src/hooks/useDeviceMonitor.ts
import { useCallback, useEffect, useRef } from 'react'
import { useDeviceStore } from '../stores/deviceStore'
import { useWebSocket } from './useWebSocket'

interface DeviceChangePayload {
  devices: Array<{ serial: string; type: 'android' | 'harmony' }>
  connected: string[]
  disconnected: string[]
}

/**
 * 设备监控 hook
 * 监听 WebSocket 的设备变化消息，自动更新设备列表
 */
export function useDeviceMonitor() {
  const setDevices = useDeviceStore((state) => state.setDevices)
  const initializedRef = useRef(false)

  const handleMessage = useCallback(
    (msg: { type: string; payload?: Record<string, unknown> }) => {
      if (msg.type === 'device_change' && msg.payload) {
        const payload = msg.payload as unknown as DeviceChangePayload
        const { devices, connected, disconnected } = payload

        // 更新设备列表
        setDevices(
          devices.map((d) => ({
            serial: d.serial,
            type: d.type,
            connected: true,
          }))
        )

        // 打印日志
        if (connected.length > 0) {
          console.log('设备已连接:', connected.join(', '))
        }
        if (disconnected.length > 0) {
          console.log('设备已断开:', disconnected.join(', '))
        }
      }
    },
    [setDevices]
  )

  const { connected } = useWebSocket({
    url: 'ws://localhost:8000/ws',
    onMessage: handleMessage,
  })

  // 连接成功后标记已初始化
  useEffect(() => {
    if (connected && !initializedRef.current) {
      initializedRef.current = true
      console.log('设备监控已启动')
    }
  }, [connected])

  return { connected }
}
