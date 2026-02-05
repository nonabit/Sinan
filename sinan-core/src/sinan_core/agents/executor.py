# sinan-core/src/sinan_core/agents/executor.py
"""执行决策 Agent"""
from enum import Enum
from typing import Optional, Tuple, Union
from PIL import Image
from .ui_parser import UITreeParser


class ExecutionStrategy(Enum):
    """执行策略枚举"""
    UI_TREE = "ui_tree"      # UI 树直接匹配
    LLM_SELECT = "llm_select"  # LLM 辅助选择
    VISION = "vision"        # 视觉模型识别


class ExecutionAgent:
    """执行决策 Agent，负责选择最优执行策略"""

    def __init__(self):
        self.parser = UITreeParser()
        self._vision_agent = None

    def decide_strategy(
        self,
        instruction: str,
        ui_elements: list[dict]
    ) -> Tuple[ExecutionStrategy, Optional[Union[dict, list[dict]]]]:
        """
        决定执行策略

        Args:
            instruction: 自然语言指令
            ui_elements: UI 树元素列表

        Returns:
            (策略类型, 目标元素)
        """
        # 提取指令中的关键词
        keywords = self._extract_keywords(instruction)

        # 尝试从 UI 树匹配
        candidates = []
        for keyword in keywords:
            matches = self.parser.fuzzy_match(keyword, ui_elements)
            candidates.extend(matches)

        # 去重
        seen = set()
        unique_candidates = []
        for c in candidates:
            key = str(c.get("center", []))
            if key not in seen:
                seen.add(key)
                unique_candidates.append(c)

        if len(unique_candidates) == 1:
            # 唯一匹配，直接使用 UI 树
            return ExecutionStrategy.UI_TREE, unique_candidates[0]

        if len(unique_candidates) > 1:
            # 多个候选，需要 LLM 辅助选择
            return ExecutionStrategy.LLM_SELECT, unique_candidates

        # 没有匹配，使用视觉模型
        return ExecutionStrategy.VISION, None

    def _extract_keywords(self, instruction: str) -> list[str]:
        """从指令中提取关键词"""
        # 移除常见动词
        verbs = ["点击", "点", "按", "选择", "打开", "进入", "找到", "tap", "click"]
        text = instruction
        for verb in verbs:
            text = text.replace(verb, " ")

        # 分词（简单实现）
        keywords = [w.strip() for w in text.split() if w.strip()]

        # 如果没有提取到关键词，使用原始指令
        if not keywords:
            keywords = [instruction]

        return keywords

    def _get_vision_agent(self):
        """获取或初始化视觉模型代理"""
        if self._vision_agent is None:
            from ..vision import VisionAgent
            self._vision_agent = VisionAgent(prefer_vllm=True)
            self._vision_agent.initialize()
        return self._vision_agent

    def execute_vision_strategy(
        self,
        instruction: str,
        screenshot: Image.Image
    ) -> Optional[dict]:
        """
        使用视觉模型执行策略

        Args:
            instruction: 自然语言指令
            screenshot: 屏幕截图

        Returns:
            包含 bbox 和 center 的字典，或 None
        """
        vision_agent = self._get_vision_agent()
        if not vision_agent.is_initialized():
            return None
        return vision_agent.detect_element(screenshot, instruction)
