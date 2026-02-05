#!/usr/bin/env python3
"""
鸿蒙手机测试用例：打开美团，搜索奶茶

前置条件：
1. 鸿蒙手机通过 HDC 连接电脑
2. 已安装美团 App
3. 已设置 HF_TOKEN 环境变量（用于视觉模型）

运行方式：
    export HF_TOKEN=your_token
    uv run python test_meituan_harmony.py
"""
import os
import sys
import time
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sinan_core.drivers.manager import DeviceManager
from sinan_core.vision import VisionAgent


def wait(seconds: float = 1.0):
    """等待指定秒数"""
    time.sleep(seconds)


def test_meituan_search():
    """测试美团搜索奶茶"""
    print("="*60)
    print("鸿蒙手机测试：打开美团，搜索奶茶")
    print("="*60)

    # 1. 初始化设备管理器
    print("\n1. 查找鸿蒙设备...")
    manager = DeviceManager()
    devices = manager.list_devices()

    if not devices:
        print("❌ 未找到连接的设备")
        print("   请确保手机已连接并开启了 HDC 调试")
        return False

    # 找到鸿蒙设备
    harmony_device = None
    for d in devices:
        if d.get("type") == "harmony":
            harmony_device = d
            break

    if not harmony_device:
        print("❌ 未找到鸿蒙设备")
        print(f"   发现的设备: {devices}")
        return False

    serial = harmony_device["serial"]
    print(f"✅ 找到鸿蒙设备: {serial}")

    # 2. 连接设备
    print("\n2. 连接设备...")
    device = manager.get_device(serial)
    if not device:
        print("❌ 无法获取设备实例")
        return False

    if not device.connect():
        print("❌ 无法连接设备")
        return False
    print("✅ 设备连接成功")

    # 3. 初始化视觉模型
    print("\n3. 初始化视觉模型...")
    vision_agent = VisionAgent()
    if not vision_agent.initialize():
        print("❌ 视觉模型初始化失败")
        return False
    print(f"✅ 视觉模型初始化成功 (后端: {vision_agent.backend_name})")

    # 4. 打开美团
    print("\n4. 打开美团 App...")
    # 鸿蒙使用 aa start 命令启动应用
    result = device._hdc("shell", "aa", "start", "-a", "EntryAbility", "-b", "com.sankuai.hmeituan")
    print(f"   启动命令结果: {result.returncode}")
    if result.stderr:
        print(f"   错误信息: {result.stderr}")
    print("   等待美团启动...")
    wait(5)  # 增加等待时间到5秒

    # 5. 截图并找到搜索框
    print("\n5. 查找搜索框...")
    screenshot = device.screenshot()
    screenshot.save("screenshot_1_home.png")
    print("   截图已保存: screenshot_1_home.png")

    # 使用视觉模型找到搜索框
    result = vision_agent.detect_element(screenshot, "搜索框")

    if not result:
        # 尝试其他描述
        result = vision_agent.detect_element(screenshot, "搜索按钮")

    if not result:
        print("⚠️  视觉模型未找到搜索框")
        print("   请手动查看 screenshot_1_home.png，然后修改脚本输入坐标")
        # 临时方案：使用默认坐标（搜索框在顶部导航栏）
        # 根据截图，搜索框在顶部，y 坐标应该在 150-200 左右
        width, height = screenshot.size
        center = (width // 2, int(height * 0.08))  # 屏幕顶部附近
        print(f"   使用默认位置: {center} (屏幕宽度: {width}, 高度: {height})")
    else:
        center = result["center"]
        print(f"✅ 找到搜索框，位置: {center}")

    # 6. 点击搜索框
    print("\n6. 点击搜索框...")
    print(f"   实际点击位置: ({center[0]}, {center[1]})")
    device.tap(center[0], center[1])
    wait(1)

    # 7. 输入"奶茶"
    print("\n7. 输入搜索内容...")
    device.input_text("奶茶")
    wait(1)

    # 8. 找到并点击搜索按钮
    print("\n8. 查找搜索按钮...")
    screenshot = device.screenshot()
    screenshot.save("screenshot_2_search.png")

    result = vision_agent.detect_element(screenshot, "搜索按钮")

    if not result:
        # 尝试直接点击键盘上的搜索/回车
        print("   未找到搜索按钮，尝试点击键盘回车...")
        # 获取屏幕尺寸，点击右下角区域（通常是键盘的搜索/回车键）
        width, height = screenshot.size
        # 点击屏幕右下角（键盘区域）
        search_key_x = width * 0.9
        search_key_y = height * 0.85
        device.tap(int(search_key_x), int(search_key_y))
        print(f"   点击键盘区域: ({int(search_key_x)}, {int(search_key_y)})")
    else:
        center = result["center"]
        print(f"✅ 找到搜索按钮，位置: {center}")
        device.tap(center[0], center[1])

    wait(2)

    # 9. 查看搜索结果
    print("\n9. 获取搜索结果...")
    screenshot = device.screenshot()
    screenshot.save("screenshot_3_results.png")
    print("✅ 截图已保存: screenshot_3_results.png")

    print("\n" + "="*60)
    print("测试完成!")
    print("="*60)
    print("截图文件:")
    print("  - screenshot_1_home.png: 美团首页")
    print("  - screenshot_2_search.png: 搜索页面")
    print("  - screenshot_3_results.png: 搜索结果")

    return True


def main():
    """主函数"""
    # 检查 HF_TOKEN
    if not os.environ.get("HF_TOKEN"):
        print("⚠️  警告: 未设置 HF_TOKEN 环境变量")
        print("   如需使用视觉模型，请先设置:")
        print("   export HF_TOKEN=your_token_here")
        print()

    try:
        success = test_meituan_search()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n\n用户中断测试")
        return 1
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
