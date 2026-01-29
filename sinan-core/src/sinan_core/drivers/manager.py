"""设备管理器"""
import subprocess
from typing import Optional
from .base import BaseDevice
from .android import AndroidDevice
from .harmony import HarmonyDevice


class DeviceManager:
    """设备管理器，负责设备发现和管理"""

    def __init__(self):
        self._devices: dict[str, BaseDevice] = {}

    def list_devices(self) -> list[dict]:
        """列出所有可用设备"""
        devices = []

        # 检测 Android 设备
        try:
            result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
            for line in result.stdout.strip().split("\n")[1:]:
                if "\tdevice" in line:
                    serial = line.split("\t")[0]
                    devices.append({"serial": serial, "type": "android"})
        except FileNotFoundError:
            pass

        # 检测鸿蒙设备
        try:
            result = subprocess.run(["hdc", "list", "targets"], capture_output=True, text=True)
            for line in result.stdout.strip().split("\n"):
                if line and not line.startswith("["):
                    devices.append({"serial": line.strip(), "type": "harmony"})
        except FileNotFoundError:
            pass

        return devices

    def _detect_device_type(self, serial: str) -> Optional[str]:
        """检测设备类型"""
        devices = self.list_devices()
        for d in devices:
            if d["serial"] == serial:
                return d["type"]
        return None

    def get_device(self, serial: str) -> Optional[BaseDevice]:
        """获取设备实例"""
        if serial in self._devices:
            return self._devices[serial]

        device_type = self._detect_device_type(serial)

        if device_type == "android":
            device = AndroidDevice(serial)
        elif device_type == "harmony":
            device = HarmonyDevice(serial)
        else:
            return None

        if device.connect():
            self._devices[serial] = device
            return device
        return None
