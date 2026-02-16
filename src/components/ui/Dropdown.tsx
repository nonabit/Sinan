import { Menu as BaseMenu } from '@base-ui/react/menu'
import clsx from 'clsx'
import type { ComponentPropsWithoutRef, ReactNode } from 'react'

type BaseMenuRootProps = ComponentPropsWithoutRef<typeof BaseMenu.Root>
type BaseMenuTriggerProps = ComponentPropsWithoutRef<typeof BaseMenu.Trigger>
type BaseMenuPopupProps = ComponentPropsWithoutRef<typeof BaseMenu.Popup>
type BaseMenuItemProps = ComponentPropsWithoutRef<typeof BaseMenu.Item>
type BaseMenuSeparatorProps = ComponentPropsWithoutRef<typeof BaseMenu.Separator>

export function DropdownRoot(props: BaseMenuRootProps) {
  return <BaseMenu.Root {...props} />
}

export function DropdownTrigger({
  className,
  ...props
}: BaseMenuTriggerProps) {
  return (
    <BaseMenu.Trigger
      {...props}
      className={clsx('ui-dropdown-trigger', className)}
    />
  )
}

export interface DropdownContentProps
  extends Omit<BaseMenuPopupProps, 'children'> {
  children: ReactNode
  sideOffset?: number
  withArrow?: boolean
}

export function DropdownContent({
  children,
  sideOffset = 8,
  withArrow = false,
  className,
  ...props
}: DropdownContentProps) {
  return (
    <BaseMenu.Portal>
      <BaseMenu.Positioner
        className="ui-dropdown-positioner"
        sideOffset={sideOffset}
      >
        <BaseMenu.Popup
          {...props}
          className={clsx('ui-dropdown-popup', className)}
        >
          {withArrow && (
            <BaseMenu.Arrow className="ui-dropdown-arrow">
              <svg width="10" height="6" viewBox="0 0 10 6" aria-hidden="true">
                <path d="M0 6 L5 0 L10 6 Z" fill="currentColor" />
              </svg>
            </BaseMenu.Arrow>
          )}
          {children}
        </BaseMenu.Popup>
      </BaseMenu.Positioner>
    </BaseMenu.Portal>
  )
}

export function DropdownItem({ className, ...props }: BaseMenuItemProps) {
  return <BaseMenu.Item {...props} className={clsx('ui-dropdown-item', className)} />
}

export function DropdownSeparator({
  className,
  ...props
}: BaseMenuSeparatorProps) {
  return (
    <BaseMenu.Separator
      {...props}
      className={clsx('ui-dropdown-separator', className)}
    />
  )
}

export interface DropdownProps
  extends Omit<BaseMenuRootProps, 'children'> {
  trigger: ReactNode
  children: ReactNode
  sideOffset?: number
  withArrow?: boolean
}

export function Dropdown({
  trigger,
  children,
  sideOffset,
  withArrow,
  ...props
}: DropdownProps) {
  return (
    <DropdownRoot {...props}>
      <DropdownTrigger>{trigger}</DropdownTrigger>
      <DropdownContent sideOffset={sideOffset} withArrow={withArrow}>
        {children}
      </DropdownContent>
    </DropdownRoot>
  )
}
