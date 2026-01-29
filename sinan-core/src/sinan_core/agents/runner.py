# sinan-core/src/sinan_core/agents/runner.py
"""用例执行引擎"""
import asyncio
import base64
from io import BytesIO
from typing import AsyncGenerator
from ..drivers.base import BaseDevice
from ..models.case import TestCase, TestStep


class CaseRunner:
    """用例执行器"""

    def __init__(self, device: BaseDevice):
        self.device = device

    async def run_step(self, step: TestStep) -> dict:
        """执行单个步骤"""
        result = {
            "step_id": step.step_id,
            "action": step.action,
            "success": False,
            "screenshot": None,
            "error": None,
        }

        try:
            if step.action == "tap":
                x, y = step.coordinates[0], step.coordinates[1]
                success = self.device.tap(x, y)
                result["success"] = success

            elif step.action == "swipe":
                coords = step.coordinates
                success = self.device.swipe(coords[0], coords[1], coords[2], coords[3])
                result["success"] = success

            elif step.action == "input":
                success = self.device.input_text(step.target_desc)
                result["success"] = success

            elif step.action == "wait":
                await asyncio.sleep(step.duration_ms / 1000)
                result["success"] = True

            # 截图
            await asyncio.sleep(0.5)  # 等待 UI 更新
            img = self.device.screenshot()
            if img:
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                result["screenshot"] = base64.b64encode(buffer.getvalue()).decode()

        except Exception as e:
            result["error"] = str(e)

        return result

    async def run_case(self, case: TestCase) -> AsyncGenerator[dict, None]:
        """执行完整用例，逐步返回结果"""
        case.status = "running"

        for step in case.steps:
            result = await self.run_step(step)
            yield result

            if not result["success"]:
                case.status = "failed"
                return

        case.status = "passed"
