// src/components/DeviceSelector/index.tsx
import { useEffect } from 'react'
import { Smartphone } from 'lucide-react'
import {
  DropdownContent,
  DropdownItem,
  DropdownRoot,
  DropdownTrigger,
} from '../ui'
import { useDeviceStore } from '../../stores/deviceStore'

const API_BASE = 'http://localhost:8000'

export function DeviceSelector() {
  const { devices, selectedDevice, setDevices, selectDevice } = useDeviceStore()
  const activeDevice =
    devices.find((device) => device.serial === selectedDevice) ?? devices[0]

  useEffect(() => {
    // 获取设备列表
    fetch(`${API_BASE}/api/devices`)
      .then((res) => res.json())
      .then((data) => setDevices(data))
      .catch((err) => console.error('获取设备列表失败:', err))
  }, [setDevices])

  useEffect(() => {
    if (!selectedDevice && devices.length > 0) {
      selectDevice(devices[0].serial)
    }
  }, [devices, selectedDevice, selectDevice])

  const isConnected = activeDevice?.connected ?? false

  return (
    <DropdownRoot>
      <DropdownTrigger className="device-pill">
        <div className="device-meta">
          <Smartphone size={16} />
          <span>{activeDevice?.serial ?? 'No device'}</span>
        </div>
        <span className={`device-dot ${isConnected ? '' : 'disconnected'}`} />
        <span className={`device-status ${isConnected ? '' : 'disconnected'}`}>
          {isConnected ? 'Connected' : 'Disconnected'}
        </span>
      </DropdownTrigger>
      <DropdownContent>
        {devices.length === 0 ? (
          <div className="device-empty">未检测到设备</div>
        ) : (
          devices.map((device) => (
            <DropdownItem
              key={device.serial}
              onClick={() => selectDevice(device.serial)}
              className={selectedDevice === device.serial ? 'device-selected' : undefined}
            >
              <div className="device-item">
                <Smartphone size={16} />
                <div>
                  <div className="device-item-title">{device.serial}</div>
                  <div className="device-item-meta">
                    {device.type === 'android' ? 'Android' : '鸿蒙'}
                  </div>
                </div>
              </div>
            </DropdownItem>
          ))
        )}
      </DropdownContent>
    </DropdownRoot>
  )
}
