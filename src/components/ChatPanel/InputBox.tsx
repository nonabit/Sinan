// src/components/ChatPanel/InputBox.tsx
import { useState, KeyboardEvent } from 'react'
import { Send, Zap } from 'lucide-react'
import { Button, Input } from '../ui'

interface InputBoxProps {
  onSend: (message: string) => void
  disabled?: boolean
}

export function InputBox({ onSend, disabled }: InputBoxProps) {
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSend(input.trim())
      setInput('')
    }
  }

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="chat-input-bar">
      <div className="chat-input-shell">
        <Zap size={18} color="#6366f1" className="chat-input-icon" />
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask AI to modify the test case..."
          className="chat-input-root"
          inputClassName="chat-input-field"
          disabled={disabled}
        />
        <Button
          onClick={handleSend}
          disabled={disabled || !input.trim()}
          className="chat-send-btn"
          variant="primary"
          size="sm"
        >
          <Send size={16} />
        </Button>
      </div>
    </div>
  )
}
