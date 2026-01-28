# sinan-core/tests/test_drivers_base.py
import pytest
from sinan_core.drivers.base import BaseDevice

def test_base_device_is_abstract():
    """BaseDevice 不能直接实例化"""
    with pytest.raises(TypeError):
        BaseDevice()

def test_base_device_has_required_methods():
    """BaseDevice 定义了所有必需的抽象方法"""
    required_methods = ['tap', 'swipe', 'screenshot', 'get_ui_tree', 'input_text', 'connect', 'disconnect']
    for method in required_methods:
        assert hasattr(BaseDevice, method)
