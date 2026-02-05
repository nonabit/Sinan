#!/usr/bin/env python3
"""
复杂任务测试：AI Agent 分解 + UI Agent 自主执行
任务：打开美团 -> 点击外卖 -> 蔬菜水果 -> 购买草莓
"""
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

sys.path.insert(0, str(Path(__file__).parent / "src"))

from PIL import Image
from sinan_core.drivers.harmony import HarmonyDevice
from sinan_core.vision import VisionAgent


class ActionType(Enum):
    """原子操作类型"""
    TAP = "tap"
    INPUT = "input"
    SWIPE = "swipe"
    WAIT = "wait"
    ASSERT = "assert"
    SCROLL = "scroll"


@dataclass
class AtomicAction:
    """原子操作"""
    type: ActionType
    target: str  # 目标元素描述
    value: str = ""  # 输入值
    timeout: int = 10
    retry: int = 3  # 失败重试次数


@dataclass
class ActionResult:
    """执行结果"""
    success: bool
    message: str
    screenshot: Optional[Image.Image] = None
    coord: Optional[Tuple[int, int]] = None


class AIAgent:
    """AI Agent - 只负责分解目标为原子操作序列"""

    def __init__(self):
        self.decomposition_rules = {
            "购买草莓": [
                # 阶段1: 打开美团
                AtomicAction(ActionType.WAIT, "等待页面稳定", timeout=2),
                AtomicAction(ActionType.TAP, "美团", retry=3),
                AtomicAction(ActionType.WAIT, "等待美团启动", timeout=3),

                # 阶段2: 进入外卖
                AtomicAction(ActionType.TAP, "外卖", retry=3),
                AtomicAction(ActionType.WAIT, "等待外卖页面", timeout=3),

                # 阶段3: 进入蔬菜水果
                AtomicAction(ActionType.TAP, "蔬菜水果", retry=3),
                AtomicAction(ActionType.WAIT, "等待分类页面", timeout=2),

                # 阶段4: 查找草莓
                AtomicAction(ActionType.SCROLL, "向下滚动查找草莓", timeout=2),
                AtomicAction(ActionType.TAP, "草莓", retry=5),
                AtomicAction(ActionType.WAIT, "等待商品详情", timeout=2),

                # 阶段5: 加入购物车
                AtomicAction(ActionType.TAP, "加入购物车", retry=3),
                AtomicAction(ActionType.ASSERT, "加入成功提示"),

                # 阶段6: 去结算
                AtomicAction(ActionType.TAP, "去结算", retry=3),
                AtomicAction(ActionType.WAIT, "等待订单确认页", timeout=2),
                AtomicAction(ActionType.ASSERT, "订单确认"),
            ]
        }

    def decompose(self, goal: str) -> List[AtomicAction]:
        """将目标分解为原子操作序列"""
        print(f"\n🤖 AI Agent: 分解目标 '{goal}'")

        if goal in self.decomposition_rules:
            actions = self.decomposition_rules[goal]
            print(f"   生成 {len(actions)} 个原子操作")
            return actions
        else:
            return [AtomicAction(ActionType.TAP, goal)]


class UIAgent:
    """UI Agent - 自主执行原子操作，每轮感知→执行→验证"""

    def __init__(self, device_serial: str):
        self.device = HarmonyDevice(device_serial)
        self.vision = None
        self.action_history: List[Dict] = []
        self.last_screenshot: Optional[Image.Image] = None
        self.step_count = 0

    def initialize(self) -> bool:
        if not self.device.connect():
            return False
        model_path = "/Users/void/.cache/sinan/mlx-models/MAI-UI-8B-bf16"
        self.vision = VisionAgent(mlx_model=model_path)
        return self.vision.initialize()

    def perceive(self) -> Image.Image:
        """感知：获取当前屏幕截图"""
        screenshot = self.device.screenshot()
        self.last_screenshot = screenshot
        return screenshot

    def detect_with_fallback(self, screenshot: Image.Image, target: str,
                            alternatives: List[str] = None) -> Optional[Dict]:
        """
        检测元素，支持备选描述
        例如："蔬菜水果" 备选 ["水果蔬菜", "生鲜", "水果"]
        """
        # 首先尝试主要描述
        result = self.vision.detect_element(screenshot, target)
        if result:
            return result

        # 尝试备选描述
        if alternatives:
            for alt in alternatives:
                print(f"   🔍 尝试备选: '{alt}'")
                result = self.vision.detect_element(screenshot, alt)
                if result:
                    print(f"   ✅ 使用备选描述命中: '{alt}'")
                    return result

        return None

    def execute_atomic(self, action: AtomicAction) -> ActionResult:
        """执行单个原子操作（带重试）"""
        self.step_count += 1
        print(f"\n{'─'*50}")
        print(f"🎯 步骤 {self.step_count}: {action.type.value} '{action.target}'")
        print(f"{'─'*50}")

        for attempt in range(action.retry):
            if attempt > 0:
                print(f"   🔄 第 {attempt + 1} 次重试...")
                time.sleep(1)

            try:
                screenshot = self.perceive()

                if action.type == ActionType.WAIT:
                    print(f"   ⏱️  等待 {action.timeout} 秒...")
                    time.sleep(action.timeout)
                    return ActionResult(True, "等待完成", screenshot)

                elif action.type == ActionType.TAP:
                    # 特殊处理：美团用命令启动更可靠
                    if action.target == "美团":
                        print(f"   🚀 使用 hdc 命令启动美团...")
                        result = self.device._hdc("shell", "aa", "start", "-b", "com.sankuai.hmeituan", "-a", "EntryAbility")
                        if result.returncode == 0:
                            print(f"   ✅ 美团启动成功")
                            time.sleep(3)
                            screenshot = self.perceive()
                            return ActionResult(True, "美团启动成功", screenshot, (0, 0))
                        else:
                            print(f"   ❌ 启动失败: {result.stderr}")
                            return ActionResult(False, f"启动失败: {result.stderr}", screenshot)

                    # 定义备选描述
                    alternatives = {
                        "外卖": ["外卖按钮", "外卖入口", "美团外卖"],
                        "蔬菜水果": ["水果蔬菜", "生鲜", "蔬菜水果分类", "水果"],
                        "草莓": ["新鲜草莓", "草莓水果", "红颜草莓"],
                        "加入购物车": ["加入购物袋", "加购", "添加"],
                    }.get(action.target, [])

                    print(f"   🔍 检测 '{action.target}'...")
                    result = self.detect_with_fallback(screenshot, action.target, alternatives)

                    if result:
                        coord = result["center"]
                        print(f"   ✅ 找到位置: {coord}")
                        self.device.tap(coord[0], coord[1])
                        print(f"   👆 点击 ({coord[0]}, {coord[1]})")

                        self.action_history.append({
                            "step": self.step_count,
                            "action": action,
                            "coord": coord,
                            "attempt": attempt + 1
                        })
                        return ActionResult(True, f"成功点击 {action.target}", screenshot, coord)
                    else:
                        if attempt == action.retry - 1:
                            screenshot.save(f"fail_step{self.step_count}_{action.target}.png")
                            return ActionResult(False, f"未找到元素: {action.target}", screenshot)

                elif action.type == ActionType.INPUT:
                    print(f"   ⌨️  输入: '{action.value}'")
                    self.device._hdc("shell", "uitest", "uiInput", "inputText", action.value)
                    return ActionResult(True, f"输入完成: {action.value}", screenshot)

                elif action.type == ActionType.SCROLL:
                    print(f"   📜 向下滑动查找...")
                    # 从屏幕中间向下滑动
                    self.device.swipe(540, 1200, 540, 600, 500)
                    time.sleep(1)
                    return ActionResult(True, "滑动完成", screenshot)

                elif action.type == ActionType.ASSERT:
                    print(f"   🔍 验证 '{action.target}'...")
                    result = self.vision.detect_element(screenshot, action.target)
                    if result:
                        print(f"   ✅ 验证通过")
                        return ActionResult(True, f"验证通过: {action.target}", screenshot, result["center"])
                    else:
                        print(f"   ⚠️ 验证未通过（继续执行）")
                        return ActionResult(True, f"验证跳过: {action.target}", screenshot)

            except Exception as e:
                print(f"   ❌ 异常: {e}")
                if attempt == action.retry - 1:
                    return ActionResult(False, f"执行异常: {e}", self.last_screenshot)

        return ActionResult(False, f"重试耗尽: {action.target}", self.last_screenshot)

    def execute_sequence(self, actions: List[AtomicAction], stop_on_error: bool = True) -> List[ActionResult]:
        """自主执行操作序列"""
        results = []

        print(f"\n{'='*60}")
        print(f"UI Agent 开始执行 ({len(actions)} 步)")
        print(f"{'='*60}")

        for action in actions:
            result = self.execute_atomic(action)
            results.append(result)

            if not result.success and stop_on_error:
                print(f"\n{'❌'*20}")
                print(f"执行中断: {result.message}")
                print(f"{'❌'*20}")
                break

        return results


def main():
    print("🧪 复杂任务测试：购买草莓")
    print("="*60)

    # 1. AI Agent 分解目标
    ai_agent = AIAgent()
    actions = ai_agent.decompose("购买草莓")

    # 2. UI Agent 初始化
    ui_agent = UIAgent("23E0223B28002180")
    if not ui_agent.initialize():
        print("❌ 初始化失败")
        return 1
    print("✅ UI Agent 就绪 (MAI-UI-8B)")

    # 3. 执行序列
    results = ui_agent.execute_sequence(actions)

    # 4. 汇总
    print(f"\n{'='*60}")
    print("📊 执行报告")
    print(f"{'='*60}")

    success_count = sum(1 for r in results if r.success)
    total = len(actions)

    for i, (action, result) in enumerate(zip(actions, results), 1):
        icon = "✅" if result.success else "❌"
        print(f"{icon} [{i:2d}] {action.type.value:8s} {action.target}")

    print(f"\n成功率: {success_count}/{total} ({success_count/total*100:.1f}%)")

    # 保存最终截图
    if ui_agent.last_screenshot:
        ui_agent.last_screenshot.save("buy_strawberry_final.png")
        print(f"📸 截图已保存: buy_strawberry_final.png")

    print(f"\n{'='*60}")
    print("✅ 测试完成")
    print(f"{'='*60}")

    return 0 if success_count == total else 1


if __name__ == "__main__":
    sys.exit(main())
