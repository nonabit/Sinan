"""设备相关 API 路由"""
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

    # TODO: 返回 base64 编码的图片
    return {"message": "截图功能待实现"}
