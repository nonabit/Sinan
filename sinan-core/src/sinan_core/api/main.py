"""FastAPI 主应用"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import devices

app = FastAPI(title="Sinan Core API", version="0.1.0")

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


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}
