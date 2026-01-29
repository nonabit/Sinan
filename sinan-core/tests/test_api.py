# sinan-core/tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from sinan_core.api.main import app

client = TestClient(app)


def test_health_check():
    """测试健康检查接口"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_devices():
    """测试设备列表接口"""
    response = client.get("/api/devices")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
