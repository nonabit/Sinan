# sinan-core/tests/test_device_manager.py
import pytest
from unittest.mock import Mock, patch
from sinan_core.drivers.manager import DeviceManager


def test_device_manager_list_devices():
    """测试列出所有设备"""
    manager = DeviceManager()
    devices = manager.list_devices()
    assert isinstance(devices, list)


def test_device_manager_get_device():
    """测试获取指定设备"""
    manager = DeviceManager()
    # 模拟设备类型检测和连接
    with patch.object(manager, '_detect_device_type', return_value='android'):
        with patch('sinan_core.drivers.android.AndroidDevice.connect', return_value=True):
            device = manager.get_device("emulator-5554")
            assert device is not None
