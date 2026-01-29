// src/stores/deviceStore.ts
import { create } from 'zustand'

interface Device {
  serial: string
  type: 'android' | 'harmony'
  connected: boolean
}

interface DeviceState {
  devices: Device[]
  selectedDevice: string | null
  setDevices: (devices: Device[]) => void
  selectDevice: (serial: string) => void
}

export const useDeviceStore = create<DeviceState>((set) => ({
  devices: [],
  selectedDevice: null,
  setDevices: (devices) => set({ devices }),
  selectDevice: (serial) => set({ selectedDevice: serial }),
}))
