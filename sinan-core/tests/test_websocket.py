# sinan-core/tests/test_websocket.py
"""WebSocket 服务测试"""
import pytest
from fastapi.testclient import TestClient
from sinan_core.api.main import app


def test_websocket_connection():
    """测试 WebSocket 连接"""
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        websocket.send_json({"type": "ping"})
        data = websocket.receive_json()
        assert data["type"] == "pong"


def test_websocket_execute_without_device():
    """测试执行命令但未选择设备"""
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        websocket.send_json({
            "type": "execute",
            "payload": {"instruction": "点击设置"}
        })
        data = websocket.receive_json()
        assert data["type"] == "error"
        assert "未选择设备" in data["payload"]["message"]
