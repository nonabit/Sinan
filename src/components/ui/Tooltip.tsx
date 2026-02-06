import * as BaseTooltip from '@base-ui/react/tooltip'
import clsx from 'clsx'
import type { ComponentPropsWithoutRef, ReactNode } from 'react'

type BaseTooltipRootProps = ComponentPropsWithoutRef<typeof BaseTooltip.Root>
type BaseTooltipTriggerProps = ComponentPropsWithoutRef<typeof BaseTooltip.Trigger>
type BaseTooltipPopupProps = ComponentPropsWithoutRef<typeof BaseTooltip.Popup>

export const TooltipProvider = BaseTooltip.Provider

export function TooltipRoot(props: BaseTooltipRootProps) {
  return <BaseTooltip.Root {...props} />
}

export function TooltipTrigger({
  className,
  ...props
}: BaseTooltipTriggerProps) {
  return (
    <BaseTooltip.Trigger
      {...props}
      className={clsx('ui-tooltip-trigger', className)}
    />
  )
}

export interface TooltipContentProps
  extends Omit<BaseTooltipPopupProps, 'children'> {
  children: ReactNode
  sideOffset?: number
  withArrow?: boolean
}

export function TooltipContent({
  children,
  sideOffset = 8,
  withArrow = true,
  className,
  ...props
}: TooltipContentProps) {
  return (
    <BaseTooltip.Portal>
      <BaseTooltip.Positioner sideOffset={sideOffset}>
        <BaseTooltip.Popup
          {...props}
          className={clsx('ui-tooltip-popup', className)}
        >
          {withArrow && (
            <BaseTooltip.Arrow className="ui-tooltip-arrow">
              <svg width="10" height="6" viewBox="0 0 10 6" aria-hidden="true">
                <path d="M0 6 L5 0 L10 6 Z" fill="currentColor" />
              </svg>
            </BaseTooltip.Arrow>
          )}
          <div className="ui-tooltip-content">{children}</div>
        </BaseTooltip.Popup>
      </BaseTooltip.Positioner>
    </BaseTooltip.Portal>
  )
}

export interface TooltipProps
  extends Omit<BaseTooltipRootProps, 'children'> {
  content: ReactNode
  children: ReactNode
  sideOffset?: number
  withArrow?: boolean
}

export function Tooltip({
  content,
  children,
  sideOffset,
  withArrow,
  ...props
}: TooltipProps) {
  return (
    <TooltipRoot {...props}>
      <TooltipTrigger>{children}</TooltipTrigger>
      <TooltipContent sideOffset={sideOffset} withArrow={withArrow}>
        {content}
      </TooltipContent>
    </TooltipRoot>
  )
}
