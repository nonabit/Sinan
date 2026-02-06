import { Input as BaseInput } from '@base-ui/react/input'
import clsx from 'clsx'
import type { ComponentPropsWithoutRef, ReactNode } from 'react'

type BaseInputProps = ComponentPropsWithoutRef<typeof BaseInput>

export interface InputProps
  extends Omit<BaseInputProps, 'className'> {
  label?: string
  helperText?: string
  error?: boolean
  inputClassName?: string
  startAdornment?: ReactNode
  endAdornment?: ReactNode
}

export function Input({
  label,
  helperText,
  error,
  className,
  inputClassName,
  startAdornment,
  endAdornment,
  ...props
}: InputProps) {
  const input = (
    <div className={clsx('ui-input-root', error && 'is-error', className)}>
      {startAdornment}
      <BaseInput
        {...props}
        className={clsx('ui-input', inputClassName)}
      />
      {endAdornment}
    </div>
  )

  if (!label && !helperText) {
    return input
  }

  return (
    <label className="ui-field">
      {label && <span className="ui-field-label">{label}</span>}
      {input}
      {helperText && (
        <span className={clsx('ui-field-help', error && 'is-error')}>
          {helperText}
        </span>
      )}
    </label>
  )
}
