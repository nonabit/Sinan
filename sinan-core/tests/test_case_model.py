# sinan-core/tests/test_case_model.py
"""测试用例数据模型测试"""
import pytest
import json
from sinan_core.models.case import TestCase, TestStep


def test_create_test_case():
    """测试创建测试用例"""
    case = TestCase(
        case_id="tc_001",
        case_name="修改字体大小",
    )
    assert case.case_id == "tc_001"
    assert len(case.steps) == 0


def test_add_step():
    """测试添加步骤"""
    case = TestCase(case_id="tc_001", case_name="测试")
    step = TestStep(
        step_id=1,
        action="tap",
        target_desc="设置图标",
        coordinates=[100, 200],
    )
    case.add_step(step)

    assert len(case.steps) == 1
    assert case.steps[0].action == "tap"


def test_case_to_json():
    """测试用例序列化为 JSON"""
    case = TestCase(case_id="tc_001", case_name="测试")
    case.add_step(TestStep(step_id=1, action="tap", target_desc="设置", coordinates=[100, 200]))

    json_str = case.to_json()
    data = json.loads(json_str)

    assert data["case_id"] == "tc_001"
    assert len(data["steps"]) == 1


def test_case_from_json():
    """测试从 JSON 创建用例"""
    json_str = '''
    {
        "case_id": "tc_002",
        "case_name": "测试用例",
        "steps": [
            {"step_id": 1, "action": "tap", "target_desc": "按钮", "coordinates": [50, 50]}
        ],
        "status": "pending"
    }
    '''
    case = TestCase.from_json(json_str)

    assert case.case_id == "tc_002"
    assert len(case.steps) == 1
    assert case.steps[0].target_desc == "按钮"
