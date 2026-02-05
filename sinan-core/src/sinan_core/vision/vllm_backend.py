# sinan-core/src/sinan_core/vision/vllm_backend.py
"""vLLM 后端 - 通过 OpenAI 兼容 API 调用 MAI-UI-8B"""
import base64
import json
import re
from io import BytesIO
from typing import Optional
from PIL import Image


class VLLMBackend:
    """vLLM 后端，通过 OpenAI 兼容 API 调用视觉模型"""

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8001/v1",
        model_name: str = "MAI-UI-8B"
    ):
        self.base_url = base_url
        self.model_name = model_name
        self.client = None

    def initialize(self) -> bool:
        """初始化 vLLM 客户端"""
        try:
            from openai import OpenAI
            self.client = OpenAI(base_url=self.base_url, api_key="dummy")
            # 测试连接
            self.client.models.list()
            return True
        except Exception:
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
        if not self.client:
            return None

        # 图片转 base64
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        img_b64 = base64.b64encode(buffer.getvalue()).decode()

        # 构建提示词
        prompt = f"""请找到屏幕上"{instruction}"的位置。
返回 JSON 格式：{{"bbox_2d": [x1, y1, x2, y2]}}
其中 (x1, y1) 是左上角坐标，(x2, y2) 是右下角坐标。
只返回 JSON，不要其他内容。"""

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{img_b64}"}
                        },
                        {"type": "text", "text": prompt}
                    ]
                }],
                max_tokens=100,
                temperature=0.1
            )
            return self._parse_response(response.choices[0].message.content)
        except Exception:
            return None

    def _parse_response(self, content: str) -> Optional[dict]:
        """解析模型响应"""
        if not content:
            return None

        # 尝试提取 JSON
        try:
            # 尝试直接解析
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
