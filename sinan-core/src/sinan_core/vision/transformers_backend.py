# sinan-core/src/sinan_core/vision/transformers_backend.py
"""Transformers 后端 - 直接使用 transformers 推理 MAI-UI-8B"""
import json
import re
from typing import Optional
from PIL import Image


class TransformersBackend:
    """Transformers 后端，直接加载模型进行推理（备选方案）"""

    def __init__(self, model_name: str = "Tongyi-MAI/MAI-UI-8B"):
        self.model_name = model_name
        self.model = None
        self.processor = None

    def initialize(self) -> bool:
        """初始化模型和处理器"""
        try:
            import torch
            from transformers import Qwen3VLForConditionalGeneration, AutoProcessor

            self.processor = AutoProcessor.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )

            # 根据平台选择设备和精度
            if torch.cuda.is_available():
                device_map = "auto"
                dtype = torch.bfloat16
            elif torch.backends.mps.is_available():
                # Apple Silicon
                device_map = "mps"
                dtype = torch.float16
            else:
                # CPU
                device_map = "cpu"
                dtype = torch.float32

            self.model = Qwen3VLForConditionalGeneration.from_pretrained(
                self.model_name,
                torch_dtype=dtype,
                device_map=device_map,
                trust_remote_code=True
            )
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
        if not self.model or not self.processor:
            return None

        # 构建提示词
        prompt = f"""请找到屏幕上"{instruction}"的位置。
返回 JSON 格式：{{"bbox_2d": [x1, y1, x2, y2]}}
其中 (x1, y1) 是左上角坐标，(x2, y2) 是右下角坐标。
只返回 JSON，不要其他内容。"""

        try:
            # 构建消息
            messages = [{
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt}
                ]
            }]

            # 处理输入
            text = self.processor.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            inputs = self.processor(
                text=[text],
                images=[image],
                return_tensors="pt"
            )

            # 移动到模型设备
            inputs = inputs.to(self.model.device)

            # 生成
            import torch
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=100,
                    do_sample=False
                )

            # 解码
            generated_ids = outputs[:, inputs.input_ids.shape[1]:]
            response = self.processor.batch_decode(
                generated_ids,
                skip_special_tokens=True
            )[0]

            return self._parse_response(response)
        except Exception:
            return None

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
