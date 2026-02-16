# UI Design System

本项目采用 **Base UI + 本地样式系统** 的方式实现一致的 UI。所有可复用组件必须基于 `src/components/ui` 中的封装，不直接在业务组件里使用 Base UI 的底层组件。

**依赖说明**
- Base UI 官方文档示例使用 `@base-ui/react` 的导入路径
- 本项目统一使用 `@base-ui/react`，与官方文档保持一致

**目标**
- 保证 UI 一致性、可维护性与可扩展性
- 让 AI 生成的组件保持统一风格，避免风格漂移
- 兼顾精细打磨与可复用性

**设计原则**
- 组件结构来自 Base UI，样式由本地 design tokens 控制
- 业务层只组合组件，不改写组件内核样式
- 任何新增交互组件先封装，再在业务中使用

**文件位置**
- Design tokens: `src/index.css`
- Base UI 样式: `src/styles/base-ui.css`
- 组件封装: `src/components/ui`

**设计 Tokens**
| Token | 用途 |
| --- | --- |
| `--ds-bg` | 应用背景色 |
| `--ds-surface` | 面板、卡片背景 |
| `--ds-surface-muted` | 次级容器背景 |
| `--ds-fg` | 主文本颜色 |
| `--ds-muted` | 次级文本颜色 |
| `--ds-border` | 默认边框色 |
| `--ds-primary` | 主按钮、强调色 |
| `--ds-primary-foreground` | 主按钮文字色 |
| `--ds-accent` | 次强调色 |
| `--ds-danger` | 错误色 |
| `--ds-ring` | 焦点描边色 |
| `--ds-radius-sm` | 小圆角 |
| `--ds-radius` | 标准圆角 |
| `--ds-radius-lg` | 大圆角 |
| `--ds-shadow-sm` | 轻微阴影 |
| `--ds-shadow-md` | 强化阴影 |

**语义层 vs 原子层**
- 语义层是业务真正应该使用的 token（例如 `--ds-surface`、`--ds-primary`）
- 原子层是色阶和基础值（例如 `--gray-50`、`--teal-600`），只用于定义语义层
- 业务层禁止直接使用原子层

**最小原子色阶（建议）**
| Token | Hex | 用途 |
| --- | --- | --- |
| `--gray-50` | `#f8fafc` | 页面底色 |
| `--gray-100` | `#f1f5f9` | 次级容器 |
| `--gray-200` | `#e2e8f0` | 边框 |
| `--gray-500` | `#475569` | 次级文本 |
| `--gray-900` | `#0f172a` | 主文本 |
| `--indigo-600` | `#4f46e5` | 主色 |
| `--indigo-100` | `#eef2ff` | 主色浅背景 |
| `--indigo-400` | `#6366f1` | 焦点环 |
| `--red-500` | `#ef4444` | 错误色 |

**语义层映射（建议）**
| 语义 Token | 映射 |
| --- | --- |
| `--ds-bg` | `--gray-50` |
| `--ds-surface` | `#ffffff` |
| `--ds-surface-muted` | `--gray-100` |
| `--ds-fg` | `--gray-900` |
| `--ds-muted` | `--gray-500` |
| `--ds-border` | `--gray-200` |
| `--ds-primary` | `--indigo-600` |
| `--ds-primary-foreground` | `#ffffff` |
| `--ds-accent` | `--indigo-400` |
| `--ds-danger` | `--red-500` |
| `--ds-ring` | `--indigo-400` |

**组件使用规范**
- 只从 `src/components/ui` 引入基础组件
- 业务层不直接写 Base UI 的底层组件或 class 细节
- 业务层可以用 `className` 做布局与尺寸控制
- 组件内部样式只使用 tokens 和 `base-ui.css` 约定 class

**状态规范**
- `hover`、`active`、`focus-visible`、`disabled` 必须完整
- `error` 使用 `error` prop 触发，样式通过 `is-error` class
- 交互组件必须可见焦点环，避免 `outline: none`

**布局与样式分工**
- 布局用 Tailwind，组件外层允许 `className`
- 组件内部样式全部由 base-ui 样式控制
- 不在业务组件内重复定义按钮、输入框的状态样式

**字体与排版**
- 默认字体为 **Inter**，在 `src/index.css` 中统一定义
- 标题 `font-weight: 600+`，正文 `font-weight: 400-500`
- 小号说明文字使用 `--ds-muted`

**颜色使用规则**
- 主要动作使用 `primary`
- 危险动作使用 `danger`
- 辅助操作或次要文本使用 `muted`
- 不引入新的色值，除非先加入 tokens

**现有基础组件**
- `Button`
- `Checkbox`
- `Dropdown`
- `Input`
- `Switch`
- `Textarea`
- `Tooltip`
- `Select` + `SelectOption`
- `Tabs` + `TabsList` + `Tab` + `TabPanel`
- `Dialog`

**组件使用示例**
```tsx
import { Button, Input, Select, SelectOption } from '../components/ui'

<Input label="设备名称" placeholder="输入名称" />
<Select defaultValue="android" label="设备类型">
  <SelectOption value="android">Android</SelectOption>
  <SelectOption value="harmony">鸿蒙</SelectOption>
</Select>
<Button variant="primary">保存</Button>
```

**禁止事项**
- 不在业务组件中复制按钮、输入框的样式
- 不在业务组件中覆盖组件的核心 class
- 不引入新的颜色或阴影值而不进入 tokens

**新增组件流程**
1. 在 `src/components/ui` 增加封装
2. 在 `src/styles/base-ui.css` 写样式类
3. 在此文档补充组件说明
