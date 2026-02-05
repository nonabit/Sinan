# sinan-core/src/sinan_core/vision/mlx_backend.py
"""MLX 后端 - 使用 Apple MLX 框架在 Mac 上高效推理 VLM 模型"""
import json
import re
from typing import Optional
from PIL import Image


class MLXBackend:
    """MLX 后端，使用 mlx-vlm 在 Apple Silicon 上高效运行视觉语言模型"""

    def __init__(
        self,
        model_name: str = "/Users/void/.cache/sinan/mlx-models/MAI-UI-8B-bf16",
    ):
        self.model_name = model_name
        self.model = None
        self.processor = None

    def initialize(self) -> bool:
        """初始化模型和处理器"""
        try:
            # 检查是否为 Apple Silicon
            import platform
            if platform.system() != "Darwin" or platform.machine() not in ["arm64", "aarch64"]:
                print("  [MLX] 不是 Apple Silicon Mac")
                return False

            from mlx_vlm import load
            from pathlib import Path

            print(f"  [MLX] 正在加载模型和处理器: {self.model_name}")
            print(f"       (首次加载会自动下载模型，可能需要几分钟)")

            # 检查是否为本地路径
            model_path = Path(self.model_name)
            if model_path.exists():
                print(f"       使用本地模型: {model_path}")
                self.model, self.processor = load(str(model_path))
            else:
                # 从 HuggingFace 加载
                self.model, self.processor = load(self.model_name)

            print(f"  [MLX] 模型和处理器加载成功")
            return True

        except Exception as e:
            print(f"  [MLX] 初始化失败: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return False

    def detect_element(
        self,
        image: Image.Image,
        instruction: str
    ) -> Optional[dict]:
        """
        使用视觉模型检测元素位置

        Args:
            image: PIL 图像对象
            instruction: 自然语言指令，描述要找的元素

        Returns:
            包含 bbox 和 center 的字典，或 None
        """
        if not self.model or not self.processor:
            return None

        # 构建提示词（Qwen3-VL 使用 <|image_pad|> 作为图像标记）
        # 注意：2B 小模型需要用更简单的提示词
        prompt = f"""<|image_pad|>
在图片中找到"{instruction}"的位置。
直接返回坐标，格式: {{"bbox_2d": [x1, y1, x2, y2]}}"""

        try:
            from mlx_vlm import generate

            # 使用 mlx-vlm 的 generate 函数
            # 参数: model, processor, image, prompt, max_tokens, etc.
            result = generate(
                self.model,
                self.processor,
                image=image,
                prompt=prompt,
                max_tokens=50,
                verbose=False
            )

            # GenerationResult 对象包含 text 属性
            response_text = result.text if hasattr(result, 'text') else str(result)

            return self._parse_response(response_text)

        except Exception as e:
            print(f"  [MLX] 检测失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_raw_response(self, image: Image.Image, instruction: str) -> Optional[str]:
        """获取原始模型响应（用于调试）"""
        if not self.model or not self.processor:
            return None

        # 使用与 detect_element 相同的简化提示词
        prompt = f"""<|image_pad|>
在图片中找到"{instruction}"的位置。
直接返回坐标，格式: {{"bbox_2d": [x1, y1, x2, y2]}}"""

        try:
            from mlx_vlm import generate

            result = generate(
                self.model,
                self.processor,
                image=image,
                prompt=prompt,
                max_tokens=50,
                verbose=False
            )

            response_text = result.text if hasattr(result, 'text') else str(result)
            return response_text

        except Exception as e:
            return f"Error: {e}"

    def _parse_response(self, content: str) -> Optional[dict]:
        """解析模型响应"""
        if not content:
            return None

        # 尝试提取 JSON
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            # 尝试从文本中提取 JSON
            match = re.search(r'\{[^}]+\}', content)
            if match:
                try:
                    data = json.loads(match.group())
                except json.JSONDecodeError:
                    return None
            else:
                return None

        # 提取 bbox
        bbox = data.get("bbox_2d") or data.get("bbox")
        if not bbox or len(bbox) != 4:
            return None

        x1, y1, x2, y2 = [int(v) for v in bbox]
        center = ((x1 + x2) // 2, (y1 + y2) // 2)

        return {
            "bbox": [x1, y1, x2, y2],
            "center": center
        }
