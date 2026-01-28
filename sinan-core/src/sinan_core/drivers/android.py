"""Android 设备驱动实现"""
import subprocess
import tempfile
from pathlib import Path
from PIL import Image
from .base import BaseDevice


class AndroidDevice(BaseDevice):
    """Android 设备驱动，基于 ADB 实现"""

    def __init__(self, serial: str):
        self.serial = serial
        self._connected = False

    def _adb(self, *args: str) -> subprocess.CompletedProcess:
        """执行 adb 命令"""
        cmd = ["adb", "-s", self.serial] + list(args)
        return subprocess.run(cmd, capture_output=True, text=True)

    def connect(self) -> bool:
        """连接设备"""
        result = self._adb("get-state")
        self._connected = result.returncode == 0
        return self._connected

    def disconnect(self) -> None:
        """断开连接"""
        self._connected = False

    def tap(self, x: int, y: int) -> bool:
        """点击坐标"""
        result = self._adb("shell", "input", "tap", str(x), str(y))
        return result.returncode == 0

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> bool:
        """滑动操作"""
        result = self._adb("shell", "input", "swipe",
                          str(x1), str(y1), str(x2), str(y2), str(duration_ms))
        return result.returncode == 0

    def screenshot(self) -> Image.Image:
        """截取屏幕"""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            temp_path = f.name

        # 使用 pull 方式更可靠
        self._adb("shell", "screencap", "-p", "/sdcard/screen.png")
        self._adb("pull", "/sdcard/screen.png", temp_path)

        img = Image.open(temp_path)
        Path(temp_path).unlink()
        return img

    def get_ui_tree(self) -> dict:
        """获取 UI 树"""
        self._adb("shell", "uiautomator", "dump", "/sdcard/ui.xml")
        result = self._adb("shell", "cat", "/sdcard/ui.xml")
        # TODO: 解析 XML 为 dict
        return {"raw_xml": result.stdout}

    def input_text(self, text: str) -> bool:
        """输入文本"""
        # 转义特殊字符
        escaped = text.replace(" ", "%s").replace("'", "\\'")
        result = self._adb("shell", "input", "text", escaped)
        return result.returncode == 0
