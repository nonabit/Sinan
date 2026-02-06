import * as BaseDialog from '@base-ui/react/dialog'
import clsx from 'clsx'
import type { ReactNode } from 'react'

export interface DialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  title?: string
  description?: string
  children?: ReactNode
  actions?: ReactNode
  className?: string
}

export function Dialog({
  open,
  onOpenChange,
  title,
  description,
  children,
  actions,
  className,
}: DialogProps) {
  return (
    <BaseDialog.Root open={open} onOpenChange={onOpenChange}>
      <BaseDialog.Portal>
        <BaseDialog.Backdrop className="ui-dialog-backdrop" />
        <BaseDialog.Viewport className="ui-dialog-viewport">
          <BaseDialog.Popup className={clsx('ui-dialog-popup', className)}>
            {title && (
              <BaseDialog.Title className="ui-dialog-title">
                {title}
              </BaseDialog.Title>
            )}
            {description && (
              <BaseDialog.Description className="ui-dialog-description">
                {description}
              </BaseDialog.Description>
            )}
            {children && <div className="ui-dialog-body">{children}</div>}
            {actions && <div className="ui-dialog-actions">{actions}</div>}
          </BaseDialog.Popup>
        </BaseDialog.Viewport>
      </BaseDialog.Portal>
    </BaseDialog.Root>
  )
}
