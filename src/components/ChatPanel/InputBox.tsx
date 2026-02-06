// src/components/ChatPanel/InputBox.tsx
import { useState, KeyboardEvent } from 'react'
import { Send } from 'lucide-react'
import { Button, Textarea } from '../ui'

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
    <div className="border-t p-4">
      <div className="flex items-center gap-2">
        <Textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="输入测试指令..."
          className="ui-textarea--compact flex-1"
          minRows={1}
          disabled={disabled}
        />
        <Button
          onClick={handleSend}
          disabled={disabled || !input.trim()}
          size="sm"
          variant="primary"
        >
          <Send size={18} />
        </Button>
      </div>
    </div>
  )
}
