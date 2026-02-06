import { useCallback, useMemo } from 'react'
import type { Connection, Edge, Node } from 'reactflow'
import { addEdge, useEdgesState, useNodesState } from 'reactflow'
import './App.css'
import { AssistantPanel } from './components/sinan-ui/assistant/AssistantPanel'
import { ChatBubble } from './components/sinan-ui/assistant/ChatBubble'
import { Composer } from './components/sinan-ui/assistant/Composer'
import { ExecutionPlan } from './components/sinan-ui/assistant/ExecutionPlan'
import { DashedEdge } from './components/sinan-ui/canvas/DashedEdge'
import { DeviceNodeCard } from './components/sinan-ui/canvas/DeviceNodeCard'
import { FlowCanvas } from './components/sinan-ui/canvas/FlowCanvas'
import { FlowNodeCard } from './components/sinan-ui/canvas/FlowNodeCard'
import { layoutNodes } from './components/sinan-ui/canvas/layout'
import { AppShell } from './components/sinan-ui/layout/AppShell'
import { TopBar } from './components/sinan-ui/layout/TopBar'
import { Workspace } from './components/sinan-ui/layout/Workspace'

function App() {
  const nodeTypes = useMemo(
    () => ({
      flow: FlowNodeCard,
      device: DeviceNodeCard,
    }),
    [],
  )

  const edgeTypes = useMemo(
    () => ({
      dashed: DashedEdge,
    }),
    [],
  )

  const initialNodes = useMemo<Node[]>(
    () => [
      {
        id: 'start-session',
        type: 'flow',
        data: {
          title: 'Start Session',
          status: 'success',
          bodyLines: [
            'Initialize Android environment',
            <span key="config">
              Load config: <strong>Prod_Env_A</strong>
            </span>,
          ],
        },
        position: { x: 0, y: 0 },
      },
      {
        id: 'device-screen',
        type: 'device',
        data: { footerText: 'Tap "Login"' },
        position: { x: 0, y: 0 },
      },
      {
        id: 'verify-dashboard',
        type: 'flow',
        data: {
          title: 'Verify Dashboard',
          status: 'running',
          bodyLines: ['Check element visibility', 'ID: #dashboard_root'],
        },
        position: { x: 0, y: 0 },
      },
    ],
    [],
  )

  const initialEdges = useMemo<Edge[]>(
    () => [
      {
        id: 'edge-start-device',
        source: 'start-session',
        target: 'device-screen',
        type: 'dashed',
      },
      {
        id: 'edge-device-verify',
        source: 'device-screen',
        target: 'verify-dashboard',
        type: 'dashed',
      },
    ],
    [],
  )

  const layoutedNodes = useMemo(() => layoutNodes(initialNodes, initialEdges), [initialEdges, initialNodes])
  const [nodes, setNodes, onNodesChange] = useNodesState(layoutedNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)

  const handleConnect = useCallback(
    (connection: Connection) => {
      setEdges((eds) => addEdge({ ...connection, type: 'dashed' }, eds))
    },
    [setEdges],
  )

  const handleLayout = useCallback(() => {
    setNodes((currentNodes) => layoutNodes(currentNodes, edges))
  }, [edges, setNodes])

  const planSteps = [
    {
      id: 'init-session',
      status: 'success' as const,
      title: 'Initialize Session',
      subtitle: 'Environment setup complete (2.1s)',
    },
    {
      id: 'navigate-login',
      status: 'success' as const,
      title: 'Navigate to Login',
      subtitle: 'Element found and tapped',
    },
    {
      id: 'verify-dashboard',
      status: 'running' as const,
      title: 'Verify Dashboard Load',
      subtitle: 'Waiting for network idle...',
    },
  ]

  return (
    <AppShell>
      <TopBar
        deviceName="Pixel 7 Pro"
        deviceStatus="Connected"
        title="Sinan Automated Testing / Checkout Flow v2.4"
        action={(
          <button className="export-button" type="button">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path
                d="M12 3v10m0 0 3.5-3.5M12 13 8.5 9.5M5 15v3a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-3"
                fill="none"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="1.6"
              />
            </svg>
            Export Report
          </button>
        )}
      />

      <Workspace>
        <FlowCanvas
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={handleConnect}
          onLayout={handleLayout}
          nodeTypes={nodeTypes}
          edgeTypes={edgeTypes}
        />

        <AssistantPanel
          title="AI Test Assistant"
          icon={(
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path
                d="M12 3 13.6 8.4 19 10l-5.4 1.6L12 17l-1.6-5.4L5 10l5.4-1.6L12 3Z"
                fill="currentColor"
              />
            </svg>
          )}
          footer={<Composer placeholder="Ask AI to modify the test case..." />}
        >
          <ChatBubble
            align="right"
            text="Run the login regression suite for the new checkout flow."
          />
          <div className="chat-timestamp">10:42 AM</div>
          <ExecutionPlan
            summary={(
              <span>
                I&apos;m running the <strong>Checkout Flow v2.4</strong> suite on the connected Pixel 7
                Pro. Here is the real-time execution plan:
              </span>
            )}
            steps={planSteps}
          />
          <div className="analysis-text">Analyzing screenshot for anomalies...</div>
        </AssistantPanel>
      </Workspace>
    </AppShell>
  )
}

export default App
