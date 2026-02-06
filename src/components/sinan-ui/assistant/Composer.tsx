interface ComposerProps {
  placeholder: string
}

export function Composer({ placeholder }: ComposerProps) {
  return (
    <div className="composer">
      <div className="composer-input">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path
            d="M12 2 9.6 7.4 4 9l5.6 1.6L12 16l2.4-5.4L20 9l-5.6-1.6L12 2Z"
            fill="currentColor"
          />
        </svg>
        {placeholder}
      </div>
      <button className="composer-send" type="button" aria-label="Send">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="m6 12 12-6-4.5 6L18 18 6 12Z" fill="currentColor" />
        </svg>
      </button>
    </div>
  )
}
