interface ChatBubbleProps {
  text: string
  align?: 'left' | 'right'
}

export function ChatBubble({ text, align = 'left' }: ChatBubbleProps) {
  return <div className={`chat-bubble ${align === 'right' ? 'right' : ''}`}>{text}</div>
}
