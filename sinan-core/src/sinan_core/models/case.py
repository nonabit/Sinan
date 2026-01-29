# sinan-core/src/sinan_core/models/case.py
"""测试用例数据模型"""
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


@dataclass
class TestStep:
    """测试步骤"""
    step_id: int
    action: str  # tap, swipe, input, wait
    target_desc: str
    coordinates: list[int] = field(default_factory=list)
    screenshot_ref: Optional[str] = None
    strategy_used: str = "ui_tree"
    duration_ms: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TestCase:
    """测试用例"""
    case_id: str
    case_name: str
    steps: list[TestStep] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "pending"  # pending, running, passed, failed

    def add_step(self, step: TestStep):
        """添加步骤"""
        self.steps.append(step)

    def to_dict(self) -> dict:
        return {
            "case_id": self.case_id,
            "case_name": self.case_name,
            "steps": [s.to_dict() for s in self.steps],
            "created_at": self.created_at,
            "status": self.status,
        }

    def to_json(self) -> str:
        """序列化为 JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "TestCase":
        """从字典创建"""
        steps = [TestStep(**s) for s in data.get("steps", [])]
        return cls(
            case_id=data["case_id"],
            case_name=data["case_name"],
            steps=steps,
            created_at=data.get("created_at", datetime.now().isoformat()),
            status=data.get("status", "pending"),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "TestCase":
        """从 JSON 创建"""
        return cls.from_dict(json.loads(json_str))
