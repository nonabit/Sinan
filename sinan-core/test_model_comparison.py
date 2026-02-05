#!/usr/bin/env python3
"""
模型对比测试：本地 MLX 2B vs 云端百炼 Qwen3-VL

使用同一张图片，对比两个模型的识别效果
"""
import os
import sys
import base64
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent / "src"))

from sinan_core.vision import VisionAgent


def test_local_mlx(image_path: str, instruction: str):
    """测试本地 MLX 模型"""
    print("\n" + "="*60)
    print("模型 1: 本地 MLX (MAI-UI-2B-bf16)")
    print("="*60)

    vision_agent = VisionAgent()
    if not vision_agent.initialize():
        print("❌ MLX 模型初始化失败")
        return None

    print(f"后端: {vision_agent.backend_name}")

    image = Image.open(image_path)
    result = vision_agent.detect_element(image, instruction)

    # 获取原始响应（不经过任何处理）
    from sinan_core.vision.mlx_backend import MLXBackend
    backend = MLXBackend()
    backend.initialize()

    # 直接调用底层的 generate 获取原始输出
    from mlx_vlm import generate
    prompt = f"""<|image_pad|>
在图片中找到"{instruction}"的位置。
直接返回坐标，格式: {{"bbox_2d": [x1, y1, x2, y2]}}"""

    result_obj = generate(
        backend.model,
        backend.processor,
        image=image,
        prompt=prompt,
        max_tokens=50,
        verbose=False
    )

    # 打印所有可能的属性
    print(f"指令: {instruction}")
    print(f"result 类型: {type(result_obj)}")
    print(f"result 属性: {dir(result_obj)}")
    print(f"result.text: {repr(result_obj.text) if hasattr(result_obj, 'text') else 'N/A'}")
    print(f"原始响应 repr: {repr(result_obj)}")
    print(f"解析结果: {result}")

    return result


def test_cloud_qwen(image_path: str, instruction: str):
    """测试云端 Qwen3-VL 模型"""
    print("\n" + "="*60)
    print("模型 2: 云端 Qwen3-VL (DashScope)")
    print("="*60)

    # 从环境变量获取 API key
    api_key = os.environ.get("QWEN_API_KEY", "")
    base_url = os.environ.get("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

    if not api_key:
        print("❌ 未设置 QWEN_API_KEY 环境变量")
        print("   请先设置: export QWEN_API_KEY=your_key")
        return None

    try:
        from openai import OpenAI

        # DashScope 配置
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

        # 读取图片并转为 base64
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode()

        prompt = f"""请找到屏幕上"{instruction}"的位置。
返回 JSON 格式：{{"bbox_2d": [x1, y1, x2, y2]}}
其中 (x1, y1) 是左上角坐标，(x2, y2) 是右下角坐标。
只返回 JSON，不要其他内容。"""

        response = client.chat.completions.create(
            model="qwen3-vl-plus",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}},
                    {"type": "text", "text": prompt}
                ]
            }],
            max_tokens=100
        )

        raw_text = response.choices[0].message.content
        print(f"指令: {instruction}")
        print(f"原始响应: {raw_text}")

        # 解析结果
        import json
        import re

        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError:
            match = re.search(r'\{[^}]+\}', raw_text)
            if match:
                data = json.loads(match.group())
            else:
                data = None

        if data:
            bbox = data.get("bbox_2d") or data.get("bbox")
            if bbox and len(bbox) == 4:
                x1, y1, x2, y2 = [int(v) for v in bbox]
                center = ((x1 + x2) // 2, (y1 + y2) // 2)
                result = {"bbox": bbox, "center": center}
                print(f"解析结果: {result}")
                return result

        print("解析结果: None")
        return None

    except Exception as e:
        print(f"❌ 百炼平台调用失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """主函数"""
    # 使用已有的截图
    image_path = "screenshot_1_home.png"

    if not Path(image_path).exists():
        print(f"❌ 图片不存在: {image_path}")
        print("   请先运行 test_meituan_harmony.py 生成截图")
        return 1

    print("="*60)
    print("模型对比测试")
    print("="*60)
    print(f"测试图片: {image_path}")
    print(f"图片尺寸: {Image.open(image_path).size}")

    instruction = "搜索框"
    print(f"测试指令: {instruction}")

    # 测试本地 MLX
    mlx_result = test_local_mlx(image_path, instruction)

    # 测试云端 Qwen3-VL
    cloud_result = test_cloud_qwen(image_path, instruction)

    # 对比结果
    print("\n" + "="*60)
    print("对比总结")
    print("="*60)

    if mlx_result:
        print(f"本地 MLX:      {mlx_result['center']} (bbox: {mlx_result['bbox']})")
    else:
        print("本地 MLX:      未检测到")

    if cloud_result:
        print(f"云端 Qwen3-VL: {cloud_result['center']} (bbox: {cloud_result['bbox']})")
    else:
        print("云端 Qwen3-VL: 未检测到")

    return 0


if __name__ == "__main__":
    sys.exit(main())
