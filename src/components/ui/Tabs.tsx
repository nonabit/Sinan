import { Tabs as BaseTabs } from '@base-ui/react/tabs'
import clsx from 'clsx'
import type { ComponentPropsWithoutRef } from 'react'

type BaseTabsProps = ComponentPropsWithoutRef<typeof BaseTabs.Root>
type BaseTabsListProps = ComponentPropsWithoutRef<typeof BaseTabs.List>
type BaseTabProps = ComponentPropsWithoutRef<typeof BaseTabs.Tab>
type BaseTabPanelProps = ComponentPropsWithoutRef<typeof BaseTabs.Panel>

export function Tabs({ className, ...props }: BaseTabsProps) {
  return <BaseTabs.Root {...props} className={clsx(className)} />
}

export function TabsList({ className, ...props }: BaseTabsListProps) {
  return (
    <BaseTabs.List {...props} className={clsx('ui-tabs-list', className)} />
  )
}

export function Tab({ className, ...props }: BaseTabProps) {
  return <BaseTabs.Tab {...props} className={clsx('ui-tab', className)} />
}

export function TabPanel({ className, ...props }: BaseTabPanelProps) {
  return (
    <BaseTabs.Panel {...props} className={clsx('ui-tab-panel', className)} />
  )
}
