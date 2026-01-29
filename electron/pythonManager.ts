// electron/pythonManager.ts
import { spawn, ChildProcess } from 'child_process'
import path from 'path'
import { app } from 'electron'

let pythonProcess: ChildProcess | null = null

export function startPythonBackend(): Promise<void> {
  return new Promise((resolve, reject) => {
    const isDev = process.env.NODE_ENV === 'development'

    // Python 项目路径
    const pythonPath = isDev
      ? path.join(app.getAppPath(), '..', 'sinan-core')
      : path.join(process.resourcesPath, 'sinan-core')

    // 启动命令
    const command = isDev ? 'uv' : 'python'
    const args = isDev
      ? ['run', 'uvicorn', 'sinan_core.api.main:app', '--host', '127.0.0.1', '--port', '8000']
      : ['-m', 'uvicorn', 'sinan_core.api.main:app', '--host', '127.0.0.1', '--port', '8000']

    pythonProcess = spawn(command, args, {
      cwd: pythonPath,
      stdio: ['ignore', 'pipe', 'pipe'],
    })

    pythonProcess.stdout?.on('data', (data) => {
      console.log(`[Python] ${data}`)
      if (data.toString().includes('Uvicorn running')) {
        resolve()
      }
    })

    pythonProcess.stderr?.on('data', (data) => {
      console.error(`[Python Error] ${data}`)
    })

    pythonProcess.on('error', (err) => {
      reject(err)
    })

    // 超时处理
    setTimeout(() => {
      resolve() // 即使没有收到启动消息也继续
    }, 5000)
  })
}

export function stopPythonBackend(): void {
  if (pythonProcess) {
    pythonProcess.kill()
    pythonProcess = null
  }
}
