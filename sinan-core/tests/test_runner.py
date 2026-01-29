# sinan-core/tests/test_runner.py
"""用例执行引擎测试"""
import pytest
from unittest.mock import Mock, AsyncMock
from sinan_core.agents.runner import CaseRunner
from sinan_core.models.case import TestCase, TestStep


@pytest.fixture
def mock_device():
    device = Mock()
    device.tap.return_value = True
    device.screenshot.return_value = Mock()  # PIL Image mock
    device.get_ui_tree.return_value = {"raw_xml": "<hierarchy/>"}
    return device


@pytest.mark.asyncio
async def test_run_step(mock_device):
    """测试执行单个步骤"""
    runner = CaseRunner(mock_device)
    step = TestStep(step_id=1, action="tap", target_desc="设置", coordinates=[100, 200])

    result = await runner.run_step(step)

    assert result["success"] is True
    mock_device.tap.assert_called_once_with(100, 200)


@pytest.mark.asyncio
async def test_run_case(mock_device):
    """测试执行完整用例"""
    runner = CaseRunner(mock_device)
    case = TestCase(case_id="tc_001", case_name="测试")
    case.add_step(TestStep(step_id=1, action="tap", target_desc="设置", coordinates=[100, 200]))
    case.add_step(TestStep(step_id=2, action="tap", target_desc="显示", coordinates=[100, 300]))

    results = []
    async for result in runner.run_case(case):
        results.append(result)

    assert len(results) == 2
    assert all(r["success"] for r in results)
