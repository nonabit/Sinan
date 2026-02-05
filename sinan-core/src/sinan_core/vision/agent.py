# sinan-core/src/sinan_core/vision/agent.py
"""VisionAgent - 视觉模型代理"""
import platform
from typing import Optional
from PIL import Image


class VisionAgent:
    """
    视觉模型代理，负责管理视觉模型后端

    后端优先级（Mac Apple Silicon）：
    1. MLX 后端（最高效）
    2. vLLM 后端（通过 OpenAI API）
    3. Transformers 后端（备选方案）

    其他平台：
    1. vLLM 后端（通过 OpenAI API）
    2. Transformers 后端（备选方案）
    """

    def __init__(
        self,
        prefer_vllm: bool = True,
        vllm_url: str = "http://127.0.0.1:8001/v1",
        prefer_mlx: bool = True,
        mlx_model: str = "mlx-community/MAI-UI-2B-bf16"
    ):
        """
        初始化 VisionAgent

        Args:
            prefer_vllm: 是否优先使用 vLLM 后端
            vllm_url: vLLM 服务地址
            prefer_mlx: Mac Apple Silicon 上是否优先使用 MLX 后端
            mlx_model: MLX 模型名称
        """
        self.prefer_vllm = prefer_vllm
        self.vllm_url = vllm_url
        self.prefer_mlx = prefer_mlx
        self.mlx_model = mlx_model
        self._backend = None
        self._backend_name = None

    @property
    def backend_name(self) -> Optional[str]:
        """返回当前使用的后端名称"""
        return self._backend_name

    def _is_apple_silicon(self) -> bool:
        """检查是否为 Apple Silicon Mac"""
        return (
            platform.system() == "Darwin" and
            platform.machine() in ["arm64", "aarch64"]
        )

    def initialize(self) -> bool:
        """
        初始化视觉模型后端

        Returns:
            是否初始化成功
        """
        # 1. Mac Apple Silicon 优先尝试 MLX 后端
        if self.prefer_mlx and self._is_apple_silicon():
            try:
                from .mlx_backend import MLXBackend
                backend = MLXBackend(model_name=self.mlx_model)
                if backend.initialize():
                    self._backend = backend
                    self._backend_name = "mlx"
                    return True
            except ImportError:
                pass

        # 2. 尝试 vLLM 后端
        if self.prefer_vllm:
            try:
                from .vllm_backend import VLLMBackend
                backend = VLLMBackend(base_url=self.vllm_url)
                if backend.initialize():
                    self._backend = backend
                    self._backend_name = "vllm"
                    return True
            except ImportError:
                pass

        # 3. 回退到 transformers
        try:
            from .transformers_backend import TransformersBackend
            backend = TransformersBackend()
            if backend.initialize():
                self._backend = backend
                self._backend_name = "transformers"
                return True
        except ImportError:
            pass

        return False

    def is_initialized(self) -> bool:
        """检查是否已初始化"""
        return self._backend is not None

    def detect_element(
        self,
        image: Image.Image,
        instruction: str
    ) -> Optional[dict]:
        """
        检测元素位置

        Args:
            image: PIL 图像对象
            instruction: 自然语言指令

        Returns:
            包含 bbox 和 center 的字典，或 None
        """
        if not self._backend:
            return None
        return self._backend.detect_element(image, instruction)

    def get_click_point(
        self,
        image: Image.Image,
        instruction: str
    ) -> Optional[tuple[int, int]]:
        """
        获取点击坐标

        Args:
            image: PIL 图像对象
            instruction: 自然语言指令

        Returns:
            (x, y) 坐标元组，或 None
        """
        result = self.detect_element(image, instruction)
        if result and result.get("center"):
            return result["center"]
        return None
