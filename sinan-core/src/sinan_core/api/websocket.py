# sinan-core/src/sinan_core/api/websocket.py
"""WebSocket 处理器"""
import asyncio
import base64
from io import BytesIO
from fastapi import WebSocket, WebSocketDisconnect
from ..drivers.manager import DeviceManager
from ..agents.executor import ExecutionAgent, ExecutionStrategy
from ..agents.ui_parser import UITreeParser


device_manager = DeviceManager()
ui_parser = UITreeParser()
execution_agent = ExecutionAgent()


class ConnectionManager:
    """WebSocket 连接管理器"""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send(self, websocket: WebSocket, message: dict):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        """向所有连接广播消息"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                # 连接可能已断开，忽略错误
                pass


manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 端点处理"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")
            payload = data.get("payload", {})

            if msg_type == "ping":
                await manager.send(websocket, {"type": "pong"})

            elif msg_type == "execute":
                instruction = payload.get("instruction", "")
                device_serial = payload.get("device")

                if not device_serial:
                    await manager.send(websocket, {
                        "type": "error",
                        "payload": {"message": "未选择设备"}
                    })
                    continue

                device = device_manager.get_device(device_serial)
                if not device:
                    await manager.send(websocket, {
                        "type": "error",
                        "payload": {"message": "设备连接失败"}
                    })
                    continue

                # 获取 UI 树并解析
                ui_tree = device.get_ui_tree()
                device_type = device_manager._detect_device_type(device_serial)

                if device_type == "android":
                    ui_elements = ui_parser.parse_android(ui_tree.get("raw_xml", ""))
                elif device_type == "harmony":
                    ui_elements = ui_parser.parse_harmony(ui_tree)
                else:
                    ui_elements = []

                # 决策执行策略
                strategy, target = execution_agent.decide_strategy(instruction, ui_elements)

                if strategy == ExecutionStrategy.UI_TREE and target:
                    # 直接执行
                    x, y = target["center"]
                    await manager.send(websocket, {
                        "type": "step_start",
                        "payload": {"stepId": 1, "action": "tap", "target": target.get("text", "")}
                    })

                    success = device.tap(x, y)
                    await asyncio.sleep(0.5)

                    # 截图
                    img = device.screenshot()
                    buffer = BytesIO()
                    img.save(buffer, format="PNG")
                    screenshot_b64 = base64.b64encode(buffer.getvalue()).decode()

                    await manager.send(websocket, {
                        "type": "step_done",
                        "payload": {
                            "stepId": 1,
                            "success": success,
                            "screenshot": screenshot_b64
                        }
                    })

                    await manager.send(websocket, {
                        "type": "case_done",
                        "payload": {"result": "pass" if success else "fail"}
                    })
                else:
                    # 使用视觉模型
                    if strategy == ExecutionStrategy.VISION:
                        await manager.send(websocket, {
                            "type": "step_start",
                            "payload": {"stepId": 1, "action": "vision_detect", "target": instruction}
                        })

                        # 截图并使用视觉模型检测
                        screenshot = device.screenshot()
                        vision_result = execution_agent.execute_vision_strategy(instruction, screenshot)

                        if vision_result and vision_result.get("center"):
                            x, y = vision_result["center"]
                            success = device.tap(x, y)
                            await asyncio.sleep(0.5)

                            # 再次截图
                            img = device.screenshot()
                            buffer = BytesIO()
                            img.save(buffer, format="PNG")
                            screenshot_b64 = base64.b64encode(buffer.getvalue()).decode()

                            await manager.send(websocket, {
                                "type": "step_done",
                                "payload": {
                                    "stepId": 1,
                                    "success": success,
                                    "screenshot": screenshot_b64,
                                    "method": "vision",
                                    "bbox": vision_result.get("bbox")
                                }
                            })

                            await manager.send(websocket, {
                                "type": "case_done",
                                "payload": {"result": "pass" if success else "fail"}
                            })
                        else:
                            await manager.send(websocket, {
                                "type": "error",
                                "payload": {"message": "视觉模型无法识别目标元素"}
                            })
                    else:
                        # LLM_SELECT 策略暂不实现
                        await manager.send(websocket, {
                            "type": "error",
                            "payload": {"message": "多个候选元素，需要 LLM 辅助选择（暂未实现）"}
                        })

            elif msg_type == "stop":
                await manager.send(websocket, {
                    "type": "stopped",
                    "payload": {}
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
