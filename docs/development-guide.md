# 司南 (Sinan) 开发指南

## 环境要求

- **Node.js**: v20+
- **pnpm**: v8+
- **Python**: 3.12+
- **uv**: Python 包管理器
- **ADB**: Android 调试（可选）
- **HDC**: 鸿蒙调试（可选）

## 快速开始

### 1. 安装依赖

```bash
# 前端依赖
pnpm install

# Python 后端依赖
cd sinan-core
uv sync
cd ..
```

### 2. 启动开发环境

**方式一：分别启动前后端（推荐调试时使用）**

```bash
# 终端 1：启动 Python 后端
cd sinan-core
uv run uvicorn sinan_core.api.main:app --reload --host 127.0.0.1 --port 8000

# 终端 2：启动 Electron + React 前端
pnpm dev
```

**方式二：一键启动（Electron 自动管理后端）**

```bash
pnpm dev
```

> 注意：Electron 会自动启动 Python 后端，但调试时建议分别启动以便查看日志。

### 3. 验证服务

- **前端**：Electron 窗口自动打开
- **后端健康检查**：http://localhost:8000/health
- **API 文档**：http://localhost:8000/docs

## 常用命令

### 前端

| 命令 | 说明 |
|------|------|
| `pnpm dev` | 启动开发服务器 |
| `pnpm build` | 构建生产版本 |
| `pnpm lint` | 代码检查 |
| `pnpm preview` | 预览构建结果 |

### Python 后端

| 命令 | 说明 |
|------|------|
| `uv sync` | 安装/同步依赖 |
| `uv run pytest` | 运行测试 |
| `uv run pytest -v` | 运行测试（详细输出） |
| `uv run ruff check` | 代码检查 |
| `uv run uvicorn sinan_core.api.main:app --reload` | 启动开发服务器 |

## 项目结构

```
Sinan/
├── electron/              # Electron 主进程
│   ├── main.ts           # 主进程入口
│   ├── preload.ts        # 预加载脚本
│   └── pythonManager.ts  # Python 进程管理
├── src/                   # React 前端
│   ├── components/       # UI 组件
│   ├── hooks/            # React Hooks
│   ├── stores/           # Zustand 状态管理
│   └── services/         # API 服务
├── sinan-core/           # Python 后端
│   ├── src/sinan_core/
│   │   ├── api/          # FastAPI 路由
│   │   ├── drivers/      # 设备驱动
│   │   ├── agents/       # AI Agent
│   │   ├── models/       # 数据模型
│   │   └── storage/      # 本地存储
│   └── tests/            # 测试文件
└── docs/                  # 文档
```

## API 端点

### REST API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/api/devices` | 获取设备列表 |
| POST | `/api/devices/{serial}/tap` | 点击操作 |
| GET | `/api/devices/{serial}/screenshot` | 获取截图 |
| GET | `/api/devices/{serial}/ui-tree` | 获取 UI 树 |
| GET | `/api/cases` | 获取用例列表 |
| POST | `/api/cases` | 创建用例 |
| GET | `/api/cases/{case_id}` | 获取用例详情 |
| DELETE | `/api/cases/{case_id}` | 删除用例 |

### WebSocket

连接地址：`ws://localhost:8000/ws`

| 消息类型 | 方向 | 说明 |
|----------|------|------|
| `ping` | 发送 | 心跳检测 |
| `pong` | 接收 | 心跳响应 |
| `execute` | 发送 | 执行指令 |
| `step_start` | 接收 | 步骤开始 |
| `step_done` | 接收 | 步骤完成 |
| `case_done` | 接收 | 用例完成 |
| `error` | 接收 | 错误信息 |

## 设备连接

### Android 设备

```bash
# 查看已连接设备
adb devices

# 连接网络设备
adb connect <ip>:5555
```

### 鸿蒙设备

```bash
# 查看已连接设备
hdc list targets

# 连接设备
hdc -t <serial> shell echo ok
```

## 测试

```bash
# 运行所有测试
cd sinan-core && uv run pytest -v

# 运行特定测试
uv run pytest tests/test_api.py -v
```

## 常见问题

### 1. Python 后端启动失败

确保已安装 uv 并同步依赖：
```bash
pip install uv
cd sinan-core && uv sync
```

### 2. 前端构建失败

清理缓存后重新安装：
```bash
rm -rf node_modules
pnpm install
```

### 3. 设备未检测到

- Android：确保 ADB 已安装且设备已开启 USB 调试
- 鸿蒙：确保 HDC 已安装且设备已开启开发者模式
