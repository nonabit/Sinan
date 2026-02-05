#!/usr/bin/env python3
"""使用魔搭社区下载 MAI-UI-8B 并转换为 MLX 格式"""
import os
import sys
from pathlib import Path

# 设置魔搭缓存目录
os.environ['MODELSCOPE_CACHE'] = str(Path.home() / '.cache/modelscope')

def download_model():
    """从魔搭社区下载模型"""
    print("=" * 60)
    print("从魔搭社区下载 MAI-UI-8B 模型")
    print("=" * 60)

    try:
        from modelscope import snapshot_download
    except ImportError:
        print("❌ 未安装 modelscope")
        print("安装: uv add modelscope")
        return None

    model_dir = snapshot_download('Tongyi-MAI/MAI-UI-8B')
    print(f"✅ 模型下载完成: {model_dir}")
    return model_dir

def convert_to_mlx(model_dir: str):
    """转换为 MLX 格式"""
    print("\n" + "=" * 60)
    print("转换为 MLX BF16 格式")
    print("=" * 60)

    output_path = Path.home() / '.cache/sinan/mlx-models/MAI-UI-8B-bf16'
    output_path.mkdir(parents=True, exist_ok=True)

    # 使用 mlx_vlm.convert 转换
    import subprocess
    cmd = [
        sys.executable, '-m', 'mlx_vlm.convert',
        '--hf-path', model_dir,
        '--mlx-path', str(output_path),
        '--dtype', 'bfloat16'
    ]

    print(f"执行: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False)

    if result.returncode == 0:
        print(f"\n✅ 转换完成!")
        print(f"MLX 模型路径: {output_path}")
        return str(output_path)
    else:
        print(f"\n❌ 转换失败")
        return None

def main():
    # 1. 下载模型
    model_dir = download_model()
    if not model_dir:
        return 1

    # 2. 转换为 MLX
    mlx_path = convert_to_mlx(model_dir)
    if not mlx_path:
        return 1

    print("\n" + "=" * 60)
    print("全部完成!")
    print("=" * 60)
    print(f"MLX 模型路径: {mlx_path}")
    print("\n使用方式:")
    print(f'  backend = MLXBackend(model_name="{mlx_path}")')
    return 0

if __name__ == "__main__":
    sys.exit(main())
