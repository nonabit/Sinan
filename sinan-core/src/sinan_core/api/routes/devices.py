"""设备相关 API 路由"""
import base64
from io import BytesIO
from fastapi import APIRouter, HTTPException
from sinan_core.drivers.manager import DeviceManager

router = APIRouter(tags=["devices"])
device_manager = DeviceManager()


@router.get("/devices")
async def list_devices():
    """获取设备列表"""
    return device_manager.list_devices()


@router.post("/devices/{serial}/tap")
async def tap(serial: str, x: int, y: int):
    """点击操作"""
    device = device_manager.get_device(serial)
    if not device:
        raise HTTPException(status_code=404, detail="设备未找到")

    success = device.tap(x, y)
    return {"success": success}


@router.get("/devices/{serial}/screenshot")
async def screenshot(serial: str):
    """获取截图"""
    device = device_manager.get_device(serial)
    if not device:
        raise HTTPException(status_code=404, detail="设备未找到")

    try:
        img = device.screenshot()
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        screenshot_b64 = base64.b64encode(buffer.getvalue()).decode()
        return {"screenshot": screenshot_b64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/devices/{serial}/ui-tree")
async def get_ui_tree(serial: str):
    """获取 UI 树"""
    device = device_manager.get_device(serial)
    if not device:
        raise HTTPException(status_code=404, detail="设备未找到")

    return device.get_ui_tree()
