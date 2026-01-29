// src/components/DeviceSelector/index.tsx
import { useEffect } from 'react'
import { Smartphone } from 'lucide-react'
import { useDeviceStore } from '../../stores/deviceStore'

const API_BASE = 'http://localhost:8000'

export function DeviceSelector() {
  const { devices, selectedDevice, setDevices, selectDevice } = useDeviceStore()

  useEffect(() => {
    // 获取设备列表
    fetch(`${API_BASE}/api/devices`)
      .then((res) => res.json())
      .then((data) => setDevices(data))
      .catch((err) => console.error('获取设备列表失败:', err))
  }, [setDevices])

  return (
    <div className="p-4 border-b">
      <h3 className="text-sm font-medium text-gray-500 mb-2">选择设备</h3>
      <div className="space-y-2">
        {devices.length === 0 ? (
          <p className="text-sm text-gray-400">未检测到设备</p>
        ) : (
          devices.map((device) => (
            <button
              key={device.serial}
              onClick={() => selectDevice(device.serial)}
              className={`w-full flex items-center gap-2 p-2 rounded-lg border ${
                selectedDevice === device.serial
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:bg-gray-50'
              }`}
            >
              <Smartphone size={16} />
              <div className="text-left">
                <p className="text-sm font-medium">{device.serial}</p>
                <p className="text-xs text-gray-500">
                  {device.type === 'android' ? 'Android' : '鸿蒙'}
                </p>
              </div>
            </button>
          ))
        )}
      </div>
    </div>
  )
}
