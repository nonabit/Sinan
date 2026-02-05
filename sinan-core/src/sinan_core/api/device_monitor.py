# sinan-core/src/sinan_core/api/device_monitor.py
"""设备状态监控服务"""
import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .websocket import ConnectionManager
    from ..drivers.manager import DeviceManager


class DeviceMonitor:
    """设备监控器，定期检测设备变化并通过 WebSocket 推送"""

    def __init__(self, device_manager: "DeviceManager", ws_manager: "ConnectionManager"):
        self._device_manager = device_manager
        self._ws_manager = ws_manager
        self._last_devices: set[str] = set()
        self._running = False

    async def start(self, interval: float = 2.0):
        """启动设备监控

        Args:
            interval: 检测间隔（秒）
        """
        self._running = True
        # 初始化设备列表
        self._last_devices = {d["serial"] for d in self._device_manager.list_devices()}

        while self._running:
            await self._check_devices()
            await asyncio.sleep(interval)

    def stop(self):
        """停止设备监控"""
        self._running = False

    async def _check_devices(self):
        """检测设备变化并推送"""
        current_devices = self._device_manager.list_devices()
        current_serials = {d["serial"] for d in current_devices}

        # 检测新连接的设备
        connected = current_serials - self._last_devices
        # 检测断开的设备
        disconnected = self._last_devices - current_serials

        if connected or disconnected:
            await self._broadcast_device_change(current_devices, connected, disconnected)
            self._last_devices = current_serials

    async def _broadcast_device_change(
        self,
        devices: list[dict],
        connected: set[str],
        disconnected: set[str]
    ):
        """广播设备变化消息"""
        message = {
            "type": "device_change",
            "payload": {
                "devices": devices,
                "connected": list(connected),
                "disconnected": list(disconnected)
            }
        }
        await self._ws_manager.broadcast(message)
