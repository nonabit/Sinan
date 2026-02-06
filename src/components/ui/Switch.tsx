import * as BaseSwitch from '@base-ui/react/switch'
import clsx from 'clsx'
import type { ComponentPropsWithoutRef, ReactNode } from 'react'

type BaseSwitchRootProps = ComponentPropsWithoutRef<typeof BaseSwitch.Root>

export interface SwitchProps extends Omit<BaseSwitchRootProps, 'children'> {
  label?: ReactNode
  helperText?: string
  error?: boolean
}

export function Switch({
  label,
  helperText,
  error,
  className,
  ...props
}: SwitchProps) {
  const root = (
    <BaseSwitch.Root
      {...props}
      className={clsx('ui-switch-root', error && 'is-error', className)}
    >
      <BaseSwitch.Thumb className="ui-switch-thumb" />
    </BaseSwitch.Root>
  )

  if (!label && !helperText) {
    return root
  }

  return (
    <label className="ui-switch-field">
      <span className="ui-switch-control">
        {root}
        {label && <span className="ui-switch-text">{label}</span>}
      </span>
      {helperText && (
        <span className={clsx('ui-field-help', error && 'is-error')}>
          {helperText}
        </span>
      )}
    </label>
  )
}
