# sinan-core/src/sinan_core/api/websocket.py
"""WebSocket 处理器"""
import json
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from typing import Callable, Any


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

    async def send_message(self, websocket: WebSocket, message: dict):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


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
                await manager.send_message(websocket, {"type": "pong"})

            elif msg_type == "execute":
                # 执行用例
                device_serial = payload.get("device")
                if not device_serial:
                    await manager.send_message(websocket, {
                        "type": "error",
                        "payload": {"message": "未选择设备"}
                    })
                    continue

                case_id = payload.get("caseId")
                await manager.send_message(websocket, {
                    "type": "step_start",
                    "payload": {"caseId": case_id, "stepId": 1}
                })

            elif msg_type == "stop":
                case_id = payload.get("caseId")
                await manager.send_message(websocket, {
                    "type": "stopped",
                    "payload": {"caseId": case_id}
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
