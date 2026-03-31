/**
 * 案件相关工具函数和常量
 * 用于统一管理案件阶段、状态、费减比例等显示逻辑
 */

import type { FeeReductionRatio, CaseStageType, CaseStatusType } from '@/types/api'
import { Badge } from '@/components/ui/badge'

// ========== 类型定义 ==========

/** 预警级别类型 */
export type DeadlineLevel = 0 | 1 | 2 | 3

/** 选项类型 */
export interface SelectOption {
  value: string
  label: string
}

/** 数值选项类型 */
export interface NumericSelectOption {
  value: number
  label: string
}

// ========== 常量定义 ==========

/** 案件阶段选项（用于筛选下拉） */
export const STAGE_FILTER_OPTIONS: SelectOption[] = [
  { value: 'all', label: '全部阶段' },
  { value: '新案', label: '新案' },
  { value: '撰写中', label: '撰写中' },
  { value: '待质检', label: '待质检' },
  { value: '已定稿', label: '已定稿' },
  { value: '待递交', label: '待递交' },
  { value: '已递交-在审', label: '已递交/在审' },
  { value: '答复OA', label: '答复OA' },
  { value: '授权', label: '授权' },
  { value: '驳回', label: '驳回' },
  { value: '放弃', label: '放弃' },
  { value: '结案归档', label: '结案归档' },
]

/** 案件阶段选项（用于表单选择，不带"全部"选项） */
export const STAGE_FORM_OPTIONS: { value: CaseStageType; label: string }[] = [
  { value: '新案', label: '新案' },
  { value: '撰写中', label: '撰写中' },
  { value: '待质检', label: '待质检' },
  { value: '已定稿', label: '已定稿' },
  { value: '待递交', label: '待递交' },
  { value: '已递交-在审', label: '已递交/在审' },
  { value: '答复OA', label: '答复OA' },
  { value: '授权', label: '授权' },
  { value: '驳回', label: '驳回' },
  { value: '放弃', label: '放弃' },
  { value: '结案归档', label: '结案归档' },
]

/** 案件状态选项（用于筛选下拉） */
export const CASE_STATUS_FILTER_OPTIONS: SelectOption[] = [
  { value: 'all', label: '全部状态' },
  { value: '进行中', label: '进行中' },
  { value: '已结案', label: '已结案' },
  { value: '已终止', label: '已终止' },
  { value: '已暂停', label: '已暂停' },
]

/** 案件状态选项（用于表单选择，不带"全部"选项） */
export const CASE_STATUS_FORM_OPTIONS: { value: CaseStatusType; label: string }[] = [
  { value: '进行中', label: '进行中' },
  { value: '已结案', label: '已结案' },
  { value: '已终止', label: '已终止' },
  { value: '已暂停', label: '已暂停' },
]

/** 专利类型选项（用于筛选下拉） */
export const PATENT_TYPE_OPTIONS: SelectOption[] = [
  { value: 'all', label: '全部类型' },
  { value: '发明', label: '发明' },
  { value: '实用新型', label: '实用新型' },
  { value: '外观设计', label: '外观设计' },
]

/** 专利类型选项（用于表单选择，不带"全部"选项） */
export const PATENT_TYPE_FORM_OPTIONS: SelectOption[] = [
  { value: '发明', label: '发明' },
  { value: '实用新型', label: '实用新型' },
  { value: '外观设计', label: '外观设计' },
]

/** 费减比例显示映射 */
export const FEE_REDUCTION_OPTIONS: Record<number, string> = {
  0: '无费减',
  70: '70%',
  85: '85%',
  100: '100%',
}

/** 费减比例选项（用于表单选择） */
export const FEE_REDUCTION_FORM_OPTIONS: NumericSelectOption[] = [
  { value: 0, label: '无费减' },
  { value: 70, label: '70%' },
  { value: 85, label: '85%' },
  { value: 100, label: '100%' },
]

// ========== 样式映射 ==========

/** 案件阶段徽章样式映射 */
const STAGE_STYLES: Record<string, string> = {
  '新案': 'bg-sky-100 text-sky-700 border-sky-200',
  '撰写中': 'bg-blue-100 text-blue-700 border-blue-200',
  '已递交-在审': 'bg-indigo-100 text-indigo-700 border-indigo-200',
  '待质检': 'bg-amber-100 text-amber-700 border-amber-200',
  '待递交': 'bg-orange-100 text-orange-700 border-orange-200',
  '答复OA': 'bg-yellow-100 text-yellow-700 border-yellow-200',
  '已定稿': 'bg-emerald-100 text-emerald-700 border-emerald-200',
  '授权': 'bg-green-100 text-green-700 border-green-200',
  '结案归档': 'bg-teal-100 text-teal-700 border-teal-200',
  '驳回': 'bg-red-100 text-red-700 border-red-200',
  '放弃': 'bg-gray-100 text-gray-600 border-gray-200',
}

/** 案件状态徽章样式映射 */
const CASE_STATUS_STYLES: Record<string, string> = {
  '进行中': 'bg-blue-50 text-blue-700 border-blue-200',
  '已结案': 'bg-green-50 text-green-700 border-green-200',
  '已终止': 'bg-red-50 text-red-700 border-red-200',
  '已暂停': 'bg-yellow-50 text-yellow-700 border-yellow-200',
}

/** 案件状态图标映射 */
const CASE_STATUS_ICONS: Record<string, string> = {
  '进行中': '●',
  '已结案': '✓',
  '已终止': '✕',
  '已暂停': '⏸',
}

/** 期限预警徽章样式映射 */
const DEADLINE_VARIANTS: Record<DeadlineLevel, 'default' | 'secondary' | 'destructive' | 'outline'> = {
  0: 'secondary',
  1: 'outline',
  2: 'default',
  3: 'destructive',
}

/** 期限预警颜色映射 */
const DEADLINE_COLORS: Record<DeadlineLevel, string> = {
  0: 'text-gray-500',
  1: 'text-yellow-600 border-yellow-500',
  2: 'text-orange-600',
  3: 'text-red-600',
}

// ========== 工具函数 ==========

/**
 * 格式化日期显示
 */
export function formatDate(dateStr: string | null | undefined): string {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

/**
 * 计算剩余天数
 */
export function getDaysRemaining(deadline: string | null | undefined): { text: string | null; level: DeadlineLevel } {
  if (!deadline) return { text: null, level: 0 }

  const deadlineDate = new Date(deadline)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  deadlineDate.setHours(0, 0, 0, 0)

  const diffTime = deadlineDate.getTime() - today.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays < 0) return { text: '已过期', level: 3 }
  if (diffDays === 0) return { text: '今天', level: 3 }
  if (diffDays <= 3) return { text: `${diffDays}天`, level: 3 }
  if (diffDays <= 7) return { text: `${diffDays}天`, level: 2 }
  if (diffDays <= 14) return { text: `${diffDays}天`, level: 1 }
  return { text: `${diffDays}天`, level: 0 }
}

/**
 * 获取费减比例显示文本
 */
export function getFeeReductionLabel(ratio: FeeReductionRatio | number): string {
  return FEE_REDUCTION_OPTIONS[ratio as FeeReductionRatio] || '无费减'
}

/**
 * 获取案件阶段徽章的样式类名
 */
export function getStageBadgeClassName(stage: string): string {
  return STAGE_STYLES[stage] || 'bg-gray-100 text-gray-700 border-gray-200'
}

/**
 * 获取案件状态徽章的样式类名
 */
export function getCaseStatusBadgeClassName(caseStatus: string): string {
  return CASE_STATUS_STYLES[caseStatus] || 'bg-gray-50 text-gray-700'
}

/**
 * 获取案件状态图标
 */
export function getCaseStatusIcon(caseStatus: string): string {
  return CASE_STATUS_ICONS[caseStatus] || '○'
}

// ========== React 徽章组件 ==========

/**
 * 案件阶段徽章组件
 */
export function StageBadge({ stage }: { stage: string | undefined | null }) {
  if (!stage) return null
  return (
    <Badge variant="outline" className={getStageBadgeClassName(stage)}>
      {stage}
    </Badge>
  )
}

/**
 * 案件状态徽章组件
 */
export function CaseStatusBadge({ caseStatus }: { caseStatus: string | undefined | null }) {
  if (!caseStatus) return null
  return (
    <Badge variant="outline" className={getCaseStatusBadgeClassName(caseStatus)}>
      <span className="mr-1">{getCaseStatusIcon(caseStatus)}</span>
      {caseStatus}
    </Badge>
  )
}

/**
 * 期限预警徽章组件
 */
export function DeadlineBadge({ daysText, level }: { daysText: string | null; level: DeadlineLevel }) {
  if (!daysText) {
    return <Badge variant="secondary">无</Badge>
  }
  return (
    <Badge variant={DEADLINE_VARIANTS[level]} className={DEADLINE_COLORS[level]}>
      {daysText}
    </Badge>
  )
}
