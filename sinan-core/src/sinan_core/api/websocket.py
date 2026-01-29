# sinan-core/src/sinan_core/api/websocket.py
"""WebSocket 处理器"""
import asyncio
import base64
from io import BytesIO
from fastapi import WebSocket, WebSocketDisconnect
from ..drivers.manager import DeviceManager
from ..agents.executor import ExecutionAgent, ExecutionStrategy


device_manager = DeviceManager()
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

                # 获取 UI 树
                ui_tree = device.get_ui_tree()
                ui_elements = []  # TODO: 解析 UI 树

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
                    # 需要视觉模型（MVP 阶段暂不实现）
                    await manager.send(websocket, {
                        "type": "error",
                        "payload": {"message": "无法识别目标元素，需要视觉模型支持"}
                    })

            elif msg_type == "stop":
                await manager.send(websocket, {
                    "type": "stopped",
                    "payload": {}
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
