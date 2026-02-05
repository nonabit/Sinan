"""FastAPI 主应用"""
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from .routes import devices, cases
from .websocket import websocket_endpoint, manager, device_manager
from .device_monitor import DeviceMonitor

# 创建设备监控器
device_monitor = DeviceMonitor(device_manager, manager)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时：启动设备监控
    monitor_task = asyncio.create_task(device_monitor.start())
    yield
    # 关闭时：停止设备监控
    device_monitor.stop()
    monitor_task.cancel()
    try:
        await monitor_task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="Sinan Core API", version="0.1.0", lifespan=lifespan)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(devices.router, prefix="/api")
app.include_router(cases.router, prefix="/api")


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}


@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    """WebSocket 端点"""
    await websocket_endpoint(websocket)
