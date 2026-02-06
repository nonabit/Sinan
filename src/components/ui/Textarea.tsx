import clsx from 'clsx'
import type { TextareaHTMLAttributes } from 'react'

export interface TextareaProps
  extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string
  helperText?: string
  error?: boolean
  minRows?: number
}

export function Textarea({
  label,
  helperText,
  error,
  className,
  minRows,
  rows,
  ...props
}: TextareaProps) {
  const textarea = (
    <textarea
      {...props}
      rows={rows ?? minRows ?? 2}
      className={clsx('ui-textarea', error && 'is-error', className)}
    />
  )

  if (!label && !helperText) {
    return textarea
  }

  return (
    <label className="ui-field">
      {label && <span className="ui-field-label">{label}</span>}
      {textarea}
      {helperText && (
        <span className={clsx('ui-field-help', error && 'is-error')}>
          {helperText}
        </span>
      )}
    </label>
  )
}
