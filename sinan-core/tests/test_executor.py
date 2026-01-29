# sinan-core/tests/test_executor.py
"""执行决策 Agent 测试"""
import pytest
from sinan_core.agents.executor import ExecutionAgent, ExecutionStrategy


def test_decide_strategy_ui_tree_match():
    """测试 UI 树直接匹配策略"""
    agent = ExecutionAgent()
    ui_elements = [
        {"text": "设置", "center": [100, 50]},
        {"text": "显示", "center": [100, 100]},
    ]

    strategy, target = agent.decide_strategy("点击设置", ui_elements)

    assert strategy == ExecutionStrategy.UI_TREE
    assert target["text"] == "设置"


def test_decide_strategy_vision_fallback():
    """测试视觉模型兜底策略"""
    agent = ExecutionAgent()
    ui_elements = [
        {"text": "设置", "center": [100, 50]},
    ]

    strategy, target = agent.decide_strategy("点击那个蓝色图标", ui_elements)

    assert strategy == ExecutionStrategy.VISION
    assert target is None


def test_decide_strategy_llm_select():
    """测试 LLM 辅助选择策略（多个候选）"""
    agent = ExecutionAgent()
    ui_elements = [
        {"text": "设置", "center": [100, 50]},
        {"text": "设置中心", "center": [100, 100]},
        {"text": "高级设置", "center": [100, 150]},
    ]

    strategy, target = agent.decide_strategy("点击设置", ui_elements)

    assert strategy == ExecutionStrategy.LLM_SELECT
    assert isinstance(target, list)
    assert len(target) == 3
