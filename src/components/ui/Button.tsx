import { Button as BaseButton } from '@base-ui/react/button'
import clsx from 'clsx'
import type { ComponentPropsWithoutRef } from 'react'

type BaseButtonProps = ComponentPropsWithoutRef<typeof BaseButton>

export interface ButtonProps extends BaseButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
}

export function Button({
  variant = 'primary',
  size = 'md',
  className,
  ...props
}: ButtonProps) {
  return (
    <BaseButton
      {...props}
      className={clsx('ui-button', className)}
      data-variant={variant}
      data-size={size}
    />
  )
}
