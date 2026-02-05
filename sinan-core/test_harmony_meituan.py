#!/usr/bin/env python3
"""鸿蒙真机测试 - 打开美团搜索奶茶"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from sinan_core.drivers.harmony import HarmonyDevice
from sinan_core.vision import VisionAgent


def main():
    print("=" * 60)
    print("鸿蒙真机测试 - 美团搜索奶茶")
    print("=" * 60)

    # 1. 连接设备
    device = HarmonyDevice("23E0223B28002180")
    if not device.connect():
        print("❌ 设备连接失败")
        return 1
    print("✅ 设备已连接")

    # 2. 初始化 VisionAgent (使用 8B 模型)
    model_path = "/Users/void/.cache/sinan/mlx-models/MAI-UI-8B-bf16"
    agent = VisionAgent(mlx_model=model_path)
    if not agent.initialize():
        print("❌ VisionAgent 初始化失败")
        return 1
    print("✅ VisionAgent 初始化完成 (MAI-UI-8B)")

    # 3. 打开美团
    print("\n📱 打开美团 App...")
    result = device._hdc("shell", "aa", "start", "-b", "com.sankuai.hmeituan", "-a", "EntryAbility")
    print(f"   启动结果: {result.returncode}")
    time.sleep(5)  # 等待应用启动

    # 4. 截图并检测搜索框
    print("\n📸 截图检测搜索框...")
    screenshot = device.screenshot()
    screenshot.save("screenshot_meituan_home.png")
    print(f"   截图已保存: screenshot_meituan_home.png")

    print("\n🔍 检测搜索框位置...")
    result = agent.detect_element(screenshot, "搜索框")

    if result:
        center = result["center"]
        print(f"   ✅ 搜索框位置: {center}")

        # 点击搜索框
        print(f"   👆 点击搜索框 ({center[0]}, {center[1]})")
        device.tap(center[0], center[1])
        time.sleep(2)

        # 5. 输入"奶茶"
        print("\n⌨️  输入'奶茶'...")
        device._hdc("shell", "uitest", "uiInput", "inputText", "奶茶")
        print("   ✅ 已输入'奶茶'")
        time.sleep(2)

        # 6. 截图检测搜索按钮
        print("\n📸 截图检测搜索按钮...")
        screenshot2 = device.screenshot()
        screenshot2.save("screenshot_meituan_search.png")

        print("🔍 检测搜索按钮...")
        result2 = agent.detect_element(screenshot2, "搜索按钮")

        if result2:
            center2 = result2["center"]
            print(f"   ✅ 搜索按钮位置: {center2}")
            print(f"   👆 点击搜索 ({center2[0]}, {center2[1]})")
            device.tap(center2[0], center2[1])
        else:
            # 尝试按回车键
            print("   ⚠️ 未检测到搜索按钮，尝试按回车键")
            device._hdc("shell", "uitest", "uiInput", "keyEvent", "66")  # ENTER

        time.sleep(3)

        # 7. 最终结果截图
        print("\n📸 截取搜索结果...")
        screenshot3 = device.screenshot()
        screenshot3.save("screenshot_meituan_results.png")
        print("✅ 结果已保存: screenshot_meituan_results.png")

        # 检测列表项
        print("\n🔍 检测附近的奶茶店...")
        result3 = agent.detect_element(screenshot3, "第一个商家")
        if result3:
            print(f"   ✅ 检测到商家位置: {result3['center']}")
        else:
            print("   ⚠️ 未检测到商家")

    else:
        print("   ❌ 未检测到搜索框")
        return 1

    print("\n" + "=" * 60)
    print("✅ 测试完成!")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
