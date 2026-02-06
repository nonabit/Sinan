// electron/pythonManager.ts
import { spawn, ChildProcess } from 'child_process'
import path from 'path'
import fs from 'fs'
import { app } from 'electron'

let pythonProcess: ChildProcess | null = null

export function startPythonBackend(): Promise<boolean> {
  return new Promise((resolve, reject) => {
    let settled = false
    const resolveOnce = (started = true) => {
      if (settled) return
      settled = true
      resolve(started)
    }
    const rejectOnce = (err: Error) => {
      if (settled) return
      settled = true
      reject(err)
    }
    const isDev = process.env.NODE_ENV === 'development'

    // Python 项目路径
    const appRoot = process.env.APP_ROOT ?? app.getAppPath()
    const pythonPath = isDev ? path.join(appRoot, 'sinan-core') : path.join(process.resourcesPath, 'sinan-core')
    if (!fs.existsSync(pythonPath)) {
      console.warn(`[Python] backend path not found: ${pythonPath}`)
      resolveOnce(false)
      return
    }

    // 启动命令
    let command = isDev ? 'uv' : 'python'
    if (isDev) {
      const uvCandidates = ['/opt/homebrew/bin/uv', '/usr/local/bin/uv']
      const resolvedUv = uvCandidates.find((candidate) => fs.existsSync(candidate))
      if (resolvedUv) {
        command = resolvedUv
      }
    }
    const args = isDev
      ? ['run', 'uvicorn', 'sinan_core.api.main:app', '--host', '127.0.0.1', '--port', '8000']
      : ['-m', 'uvicorn', 'sinan_core.api.main:app', '--host', '127.0.0.1', '--port', '8000']

    pythonProcess = spawn(command, args, {
      cwd: pythonPath,
      stdio: ['ignore', 'pipe', 'pipe'],
      env: {
        ...process.env,
        PATH: `/opt/homebrew/bin:/usr/local/bin:${process.env.PATH ?? ''}`,
      },
    })

    pythonProcess.stdout?.on('data', (data) => {
      console.log(`[Python] ${data}`)
      if (data.toString().includes('Uvicorn running')) {
        resolveOnce(true)
      }
    })

    pythonProcess.stderr?.on('data', (data) => {
      console.error(`[Python Error] ${data}`)
    })

    pythonProcess.on('error', (err: NodeJS.ErrnoException) => {
      if (isDev && err.code === 'ENOENT') {
        console.warn('[Python] uv not found; skipping backend startup in dev mode.')
        resolveOnce(false)
        return
      }
      rejectOnce(err)
    })

    // 超时处理
    setTimeout(() => {
      resolveOnce(true) // 即使没有收到启动消息也继续
    }, 5000)
  })
}

export function stopPythonBackend(): void {
  if (pythonProcess) {
    pythonProcess.kill()
    pythonProcess = null
  }
}
