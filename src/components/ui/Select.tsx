import { Select as BaseSelect } from '@base-ui/react/select'
import clsx from 'clsx'
import type { ComponentPropsWithoutRef, ReactNode } from 'react'
import { useId } from 'react'

type BaseSelectRootProps = ComponentPropsWithoutRef<typeof BaseSelect.Root>
type BaseSelectItemProps = ComponentPropsWithoutRef<typeof BaseSelect.Item>

export interface SelectProps
  extends Omit<BaseSelectRootProps, 'children' | 'className'> {
  label?: string
  helperText?: string
  error?: boolean
  placeholder?: string
  className?: string
  children: ReactNode
}

export function Select({
  label,
  helperText,
  error,
  placeholder,
  className,
  children,
  ...props
}: SelectProps) {
  const labelId = useId()
  const select = (
    <BaseSelect.Root {...props}>
      <BaseSelect.Trigger
        className={clsx('ui-select-trigger', error && 'is-error', className)}
        aria-labelledby={label ? labelId : undefined}
      >
        <BaseSelect.Value
          className="ui-select-value"
          placeholder={placeholder}
        />
        <BaseSelect.Icon className="ui-select-icon">▾</BaseSelect.Icon>
      </BaseSelect.Trigger>
      <BaseSelect.Portal>
        <BaseSelect.Positioner className="ui-select-positioner" sideOffset={8}>
          <BaseSelect.Popup className="ui-select-popup">
            <BaseSelect.List className="ui-select-list">
              {children}
            </BaseSelect.List>
          </BaseSelect.Popup>
        </BaseSelect.Positioner>
      </BaseSelect.Portal>
    </BaseSelect.Root>
  )

  if (!label && !helperText) {
    return select
  }

  return (
    <div className="ui-field">
      {label && (
        <span className="ui-field-label" id={labelId}>
          {label}
        </span>
      )}
      {select}
      {helperText && (
        <span className={clsx('ui-field-help', error && 'is-error')}>
          {helperText}
        </span>
      )}
    </div>
  )
}

export function SelectOption({ className, children, ...props }: BaseSelectItemProps) {
  return (
    <BaseSelect.Item
      {...props}
      className={clsx('ui-select-item', className)}
    >
      <BaseSelect.ItemIndicator className="ui-select-item-indicator">
        ✓
      </BaseSelect.ItemIndicator>
      <BaseSelect.ItemText className="ui-select-item-text">
        {children}
      </BaseSelect.ItemText>
    </BaseSelect.Item>
  )
}
