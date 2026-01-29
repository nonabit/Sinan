// src/services/api.ts
const API_BASE = 'http://localhost:8000'

export interface Device {
  serial: string
  type: 'android' | 'harmony'
}

export interface TestCase {
  caseId: string
  caseName: string
  steps: TestStep[]
}

export interface TestStep {
  stepId: number
  action: string
  targetDesc: string
  coordinates: number[]
}

export const api = {
  // 获取设备列表
  async getDevices(): Promise<Device[]> {
    const res = await fetch(`${API_BASE}/api/devices`)
    return res.json()
  },

  // 执行点击
  async tap(serial: string, x: number, y: number): Promise<{ success: boolean }> {
    const res = await fetch(`${API_BASE}/api/devices/${serial}/tap?x=${x}&y=${y}`, {
      method: 'POST',
    })
    return res.json()
  },

  // 获取截图
  async screenshot(serial: string): Promise<{ screenshot: string }> {
    const res = await fetch(`${API_BASE}/api/devices/${serial}/screenshot`)
    return res.json()
  },
}
