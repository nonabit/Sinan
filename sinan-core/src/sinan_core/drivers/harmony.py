"""鸿蒙 Next 设备驱动实现"""
import subprocess
import tempfile
import json
from pathlib import Path
from PIL import Image
from .base import BaseDevice


class HarmonyDevice(BaseDevice):
    """鸿蒙设备驱动，基于 HDC 实现"""

    def __init__(self, serial: str):
        self.serial = serial
        self._connected = False

    def _hdc(self, *args: str) -> subprocess.CompletedProcess:
        """执行 hdc 命令"""
        cmd = ["hdc", "-t", self.serial] + list(args)
        return subprocess.run(cmd, capture_output=True, text=True)

    def connect(self) -> bool:
        """连接设备"""
        result = self._hdc("shell", "echo", "ok")
        self._connected = result.returncode == 0 and "ok" in result.stdout
        return self._connected

    def disconnect(self) -> None:
        """断开连接"""
        self._connected = False

    def tap(self, x: int, y: int) -> bool:
        """点击坐标 - 使用 uitest"""
        result = self._hdc("shell", "uitest", "uiInput", "click", str(x), str(y))
        return result.returncode == 0

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> bool:
        """滑动操作"""
        result = self._hdc(
            "shell", "uitest", "uiInput", "swipe",
            str(x1), str(y1), str(x2), str(y2), str(duration_ms)
        )
        return result.returncode == 0

    def screenshot(self) -> Image.Image:
        """截取屏幕 - 鸿蒙必须使用 .jpeg 后缀"""
        with tempfile.NamedTemporaryFile(suffix=".jpeg", delete=False) as f:
            temp_path = f.name

        # 鸿蒙 snapshot_display 要求 .jpeg 后缀
        remote_path = "/data/local/tmp/screen.jpeg"

        # 截图到设备
        result1 = self._hdc("shell", "snapshot_display", "-f", remote_path)
        if result1.returncode != 0:
            raise RuntimeError(f"截图失败: {result1.stderr}")

        # 传输到本地
        result2 = self._hdc("file", "recv", remote_path, temp_path)
        if result2.returncode != 0:
            raise RuntimeError(f"传输截图失败: {result2.stderr}")

        # 检查文件是否存在且有内容
        if not Path(temp_path).exists() or Path(temp_path).stat().st_size == 0:
            raise RuntimeError("截图文件为空或不存在")

        img = Image.open(temp_path)
        Path(temp_path).unlink()
        return img

    def get_ui_tree(self) -> dict:
        """获取 UI 树 - 使用 uitest dumpLayout"""
        remote_path = "/data/local/tmp/layout.json"
        self._hdc("shell", "uitest", "dumpLayout", "-p", remote_path)
        result = self._hdc("shell", "cat", remote_path)

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"raw": result.stdout}

    def input_text(self, text: str) -> bool:
        """输入文本"""
        result = self._hdc("shell", "uitest", "uiInput", "inputText", text)
        return result.returncode == 0
