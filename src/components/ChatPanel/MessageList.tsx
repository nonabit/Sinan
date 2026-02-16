// src/components/ChatPanel/MessageList.tsx

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

import { CheckCircle, Clock } from 'lucide-react'

interface MessageListProps {
  messages: Message[]
  isThinking?: boolean
}

export function MessageList({ messages, isThinking }: MessageListProps) {
  return (
    <div className="chat-body">
      {messages.map((msg) => {
        const isUser = msg.role === 'user'

        if (!isUser && msg.content === 'suite-status') {
          return (
            <div key={msg.id} className="chat-message ai">
              <div className="chat-card">
                I'm running the <strong>Checkout Flow v2.4</strong> suite on the
                connected device. Here is the real-time execution plan:
                <ul>
                  <li>
                    <span style={{ marginTop: 3, color: '#10b981' }}>
                      <CheckCircle size={16} />
                    </span>
                    <div>
                      <span className="chat-card-title">Initialize Session</span>
                      <span className="chat-card-subtitle">
                        Environment setup complete (2.1s)
                      </span>
                    </div>
                  </li>
                  <li>
                    <span style={{ marginTop: 3, color: '#10b981' }}>
                      <CheckCircle size={16} />
                    </span>
                    <div>
                      <span className="chat-card-title">Navigate to Login</span>
                      <span className="chat-card-subtitle">
                        Element found and tapped
                      </span>
                    </div>
                  </li>
                  <li>
                    <span style={{ marginTop: 3, color: '#f59e0b' }}>
                      <Clock size={16} />
                    </span>
                    <div>
                      <span className="chat-card-title">
                        Verify Dashboard Load
                      </span>
                      <span className="chat-card-subtitle">
                        Waiting for network idle...
                      </span>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          )
        }

        return (
          <div
            key={msg.id}
            className={`chat-message ${isUser ? 'user' : 'ai'}`}
          >
            <div className={`chat-bubble ${isUser ? '' : 'ai'}`}>
              <p className="whitespace-pre-wrap">{msg.content}</p>
            </div>
            <span className="chat-time">
              {msg.timestamp.toLocaleTimeString()}
            </span>
          </div>
        )
      })}

      {isThinking && (
        <div className="chat-message ai">
          <div className="thinking-row">
            <span className="thinking-dot" />
            <span className="thinking-dot" />
            <span className="thinking-dot" />
            <span className="thinking-text">
              Analyzing screenshot for anomalies...
            </span>
          </div>
        </div>
      )}
    </div>
  )
}
