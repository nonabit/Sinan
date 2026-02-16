import { Checkbox as BaseCheckbox } from '@base-ui/react/checkbox'
import clsx from 'clsx'
import type { ComponentPropsWithoutRef, ReactNode } from 'react'

type BaseCheckboxRootProps = ComponentPropsWithoutRef<typeof BaseCheckbox.Root>

export interface CheckboxProps
  extends Omit<BaseCheckboxRootProps, 'children'> {
  label?: ReactNode
  helperText?: string
  error?: boolean
  indicator?: ReactNode
}

export function Checkbox({
  label,
  helperText,
  error,
  indicator,
  className,
  ...props
}: CheckboxProps) {
  const root = (
    <BaseCheckbox.Root
      {...props}
      className={clsx('ui-checkbox-root', error && 'is-error', className)}
    >
      <BaseCheckbox.Indicator className="ui-checkbox-indicator">
        {indicator ?? (
          <svg viewBox="0 0 10 10" width="10" height="10" aria-hidden="true">
            <path
              fill="currentColor"
              d="M9.16 1.12a.75.75 0 0 1 .22 1.04L5.14 8.66a.9.9 0 0 1-1.13.15L1.25 6.31a.75.75 0 1 1 1.01-1.11L4.36 7.1l3.76-5.76a.75.75 0 0 1 1.04-.22Z"
            />
          </svg>
        )}
      </BaseCheckbox.Indicator>
    </BaseCheckbox.Root>
  )

  if (!label && !helperText) {
    return root
  }

  return (
    <label className="ui-checkbox-field">
      <span className="ui-checkbox-control">
        {root}
        {label && <span className="ui-checkbox-text">{label}</span>}
      </span>
      {helperText && (
        <span className={clsx('ui-field-help', error && 'is-error')}>
          {helperText}
        </span>
      )}
    </label>
  )
}
