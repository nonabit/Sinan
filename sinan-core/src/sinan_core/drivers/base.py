"""设备驱动抽象基类"""
from abc import ABC, abstractmethod
from PIL import Image


class BaseDevice(ABC):
    """设备驱动抽象基类，定义统一的设备操作接口"""

    @abstractmethod
    def connect(self) -> bool:
        """连接设备，返回是否成功"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """断开设备连接"""
        pass

    @abstractmethod
    def tap(self, x: int, y: int) -> bool:
        """点击指定坐标"""
        pass

    @abstractmethod
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> bool:
        """滑动操作"""
        pass

    @abstractmethod
    def screenshot(self) -> Image.Image:
        """截取屏幕，返回 PIL Image"""
        pass

    @abstractmethod
    def get_ui_tree(self) -> dict:
        """获取 UI 树结构"""
        pass

    @abstractmethod
    def input_text(self, text: str) -> bool:
        """输入文本"""
        pass
