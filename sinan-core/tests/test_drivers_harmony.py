# sinan-core/tests/test_drivers_harmony.py
import pytest
from unittest.mock import Mock, patch
from sinan_core.drivers.harmony import HarmonyDevice
from sinan_core.drivers.base import BaseDevice

def test_harmony_device_inherits_base():
    """HarmonyDevice 继承自 BaseDevice"""
    assert issubclass(HarmonyDevice, BaseDevice)

def test_harmony_device_init():
    """HarmonyDevice 初始化需要设备序列号"""
    device = HarmonyDevice(serial="FMR0223C13000649")
    assert device.serial == "FMR0223C13000649"

@patch('subprocess.run')
def test_harmony_device_connect(mock_run):
    """测试设备连接"""
    mock_run.return_value = Mock(returncode=0, stdout="ok")

    device = HarmonyDevice(serial="FMR0223C13000649")
    result = device.connect()

    assert result is True
