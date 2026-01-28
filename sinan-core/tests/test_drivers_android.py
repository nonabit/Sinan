# sinan-core/tests/test_drivers_android.py
import pytest
from unittest.mock import Mock, patch
from sinan_core.drivers.android import AndroidDevice
from sinan_core.drivers.base import BaseDevice


def test_android_device_inherits_base():
    """AndroidDevice 继承自 BaseDevice"""
    assert issubclass(AndroidDevice, BaseDevice)


def test_android_device_init():
    """AndroidDevice 初始化需要设备序列号"""
    device = AndroidDevice(serial="emulator-5554")
    assert device.serial == "emulator-5554"


@patch('subprocess.run')
def test_android_device_connect(mock_run):
    """测试设备连接"""
    mock_run.return_value = Mock(returncode=0, stdout="device")

    device = AndroidDevice(serial="127.0.0.1:5555")
    result = device.connect()

    assert result is True
