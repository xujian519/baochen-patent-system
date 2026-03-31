import { useEffect, useState } from 'react'
import { Plus, Search, RotateCcw } from 'lucide-react'
import { useCaseStore } from '@/stores/case'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { ResizablePanels } from '@/components/ui/resizable'
import { CaseDetailPanel } from './Detail'
import CaseForm from './Form'
import type { Case } from '@/types/api'

// 案件状态选项（使用 'all' 作为全部选项的值，避免空字符串）
const STATUS_OPTIONS = [
  { value: 'all', label: '全部状态' },
  { value: '新案', label: '新案' },
  { value: '在审', label: '在审' },
  { value: '已授权', label: '已授权' },
  { value: '已驳回', label: '已驳回' },
  { value: '已撤回', label: '已撤回' },
  { value: '已放弃', label: '已放弃' },
]

// 专利类型选项
const PATENT_TYPE_OPTIONS = [
  { value: 'all', label: '全部类型' },
  { value: '发明', label: '发明' },
  { value: '实用新型', label: '实用新型' },
  { value: '外观设计', label: '外观设计' },
]

// 根据期限级别返回颜色
function getDeadlineBadge(level: number, daysText: string | null) {
  if (!daysText) return <Badge variant="secondary">无</Badge>

  const variants: Record<number, 'default' | 'secondary' | 'destructive' | 'outline'> = {
    0: 'secondary',
    1: 'outline',
    2: 'default',
    3: 'destructive',
  }

  const colors: Record<number, string> = {
    0: 'text-gray-500',
    1: 'text-yellow-600 border-yellow-500',
    2: 'text-orange-600',
    3: 'text-red-600',
  }

  return (
    <Badge variant={variants[level] || 'secondary'} className={colors[level]}>
      {daysText}
    </Badge>
  )
}

// 获取状态徽章样式（11种状态，不同颜色区分）
function getStatusBadge(status: string) {
  const statusStyles: Record<string, string> = {
    // 初始状态 - 蓝色系
    '新案': 'bg-sky-100 text-sky-700 border-sky-200',
    // 进行中 - 蓝色系
    '撰写中': 'bg-blue-100 text-blue-700 border-blue-200',
    '已递交/在审': 'bg-indigo-100 text-indigo-700 border-indigo-200',
    // 等待状态 - 黄色/橙色系
    '待质检': 'bg-amber-100 text-amber-700 border-amber-200',
    '待递交': 'bg-orange-100 text-orange-700 border-orange-200',
    '答复OA': 'bg-yellow-100 text-yellow-700 border-yellow-200',
    // 完成状态 - 绿色系
    '已定稿': 'bg-emerald-100 text-emerald-700 border-emerald-200',
    '授权': 'bg-green-100 text-green-700 border-green-200',
    '结案归档': 'bg-teal-100 text-teal-700 border-teal-200',
    // 终止状态 - 红色/灰色系
    '驳回': 'bg-red-100 text-red-700 border-red-200',
    '放弃': 'bg-gray-100 text-gray-600 border-gray-200',
    // 兼容旧数据
    '在审': 'bg-indigo-100 text-indigo-700 border-indigo-200',
    '已授权': 'bg-green-100 text-green-700 border-green-200',
    '已驳回': 'bg-red-100 text-red-700 border-red-200',
    '已撤回': 'bg-gray-100 text-gray-600 border-gray-200',
  }

  return (
    <Badge
      variant="outline"
      className={statusStyles[status] || 'bg-gray-100 text-gray-700 border-gray-200'}
    >
      {status}
    </Badge>
  )
}

// 计算剩余天数
function getDaysRemaining(deadline: string | null): { text: string | null; level: number } {
  if (!deadline) return { text: null, level: 0 }

  const deadlineDate = new Date(deadline)
  const today = new Date()
  const diffTime = deadlineDate.getTime() - today.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays < 0) return { text: '已过期', level: 3 }
  if (diffDays === 0) return { text: '今天', level: 3 }
  if (diffDays <= 3) return { text: `${diffDays}天`, level: 3 }
  if (diffDays <= 7) return { text: `${diffDays}天`, level: 2 }
  if (diffDays <= 14) return { text: `${diffDays}天`, level: 1 }
  return { text: `${diffDays}天`, level: 0 }
}

export default function CaseList() {
  const {
    cases,
    total,
    page,
    pageSize,
    isLoading,
    filters,
    isDetailOpen,
    fetchCases,
    setFilters,
    resetFilters,
    setPage,
    openDetail,
    closeDetail,
    openForm,
  } = useCaseStore()

  // 本地搜索状态（用于防抖）
  const [searchInput, setSearchInput] = useState(filters.search || '')

  // 初始化加载数据
  useEffect(() => {
    fetchCases()
  }, [])

  // 搜索防抖处理
  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchInput !== filters.search) {
        setFilters({ search: searchInput })
      }
    }, 300)
    return () => clearTimeout(timer)
  }, [searchInput])

  // 计算总页数
  const totalPages = Math.ceil(total / pageSize)

  // 处理行点击
  const handleRowClick = (caseItem: Case) => {
    openDetail(caseItem.id)
  }

  return (
    <>
      <ResizablePanels
        leftPanel={
          <div className="flex h-full flex-col space-y-4 p-4">
            {/* 页面标题和操作区 */}
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-foreground">案件管理</h1>
                <p className="text-sm text-muted-foreground">
                  共 {total} 条记录
                </p>
              </div>
              <Button onClick={() => openForm('create')}>
                <Plus className="mr-2 h-4 w-4" />
                新建案件
              </Button>
            </div>

            {/* 筛选条件区 */}
            <div className="flex flex-wrap items-center gap-3 rounded-lg border bg-card p-4">
              {/* 搜索框 */}
              <div className="relative flex-1 min-w-[200px]">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  placeholder="搜索案件编号、发明名称..."
                  value={searchInput}
                  onChange={(e) => setSearchInput(e.target.value)}
                  className="pl-9"
                />
              </div>

              {/* 状态筛选 */}
              <Select
                value={filters.status || 'all'}
                onValueChange={(value) => setFilters({ status: value === 'all' ? '' : value })}
              >
                <SelectTrigger className="w-[120px]">
                  <SelectValue placeholder="状态" />
                </SelectTrigger>
                <SelectContent>
                  {STATUS_OPTIONS.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      {option.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              {/* 专利类型筛选 */}
              <Select
                value={filters.patent_type || 'all'}
                onValueChange={(value) => setFilters({ patent_type: value === 'all' ? '' : value })}
              >
                <SelectTrigger className="w-[120px]">
                  <SelectValue placeholder="类型" />
                </SelectTrigger>
                <SelectContent>
                  {PATENT_TYPE_OPTIONS.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      {option.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              {/* 重置按钮 */}
              <Button
                variant="outline"
                size="icon"
                onClick={() => {
                  setSearchInput('')
                  resetFilters()
                }}
                title="重置筛选"
              >
                <RotateCcw className="h-4 w-4" />
              </Button>
            </div>

            {/* 数据表格 */}
            <div className="flex-1 overflow-auto rounded-lg border bg-card">
              <Table>
                <TableHeader>
                  <TableRow className="bg-muted/50">
                    <TableHead className="w-[140px]">案件编号</TableHead>
                    <TableHead className="min-w-[200px]">发明名称</TableHead>
                    <TableHead className="w-[80px]">类型</TableHead>
                    <TableHead className="w-[120px]">客户</TableHead>
                    <TableHead className="w-[80px]">状态</TableHead>
                    <TableHead className="w-[100px]">最近期限</TableHead>
                    <TableHead className="w-[100px]">代理师</TableHead>
                    <TableHead className="w-[100px]">创建时间</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {isLoading ? (
                    <TableRow>
                      <TableCell colSpan={8} className="h-24 text-center">
                        <div className="flex items-center justify-center">
                          <div className="h-6 w-6 animate-spin rounded-full border-2 border-primary border-t-transparent" />
                          <span className="ml-2 text-muted-foreground">加载中...</span>
                        </div>
                      </TableCell>
                    </TableRow>
                  ) : cases.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={8} className="h-24 text-center text-muted-foreground">
                        暂无数据
                      </TableCell>
                    </TableRow>
                  ) : (
                    cases.map((caseItem) => {
                      const deadline = getDaysRemaining(caseItem.nearest_deadline)
                      return (
                        <TableRow
                          key={caseItem.id}
                          className="cursor-pointer hover:bg-muted/50"
                          onClick={() => handleRowClick(caseItem)}
                        >
                          <TableCell className="font-mono text-sm">
                            {caseItem.case_number}
                          </TableCell>
                          <TableCell className="font-medium">
                            <div className="truncate max-w-[300px]" title={caseItem.title}>
                              {caseItem.title}
                            </div>
                          </TableCell>
                          <TableCell>
                            <Badge variant="outline">{caseItem.patent_type}</Badge>
                          </TableCell>
                          <TableCell>
                            <div className="truncate max-w-[120px]" title={caseItem.client?.name}>
                              {caseItem.client?.short_name || caseItem.client?.name || '-'}
                            </div>
                          </TableCell>
                          <TableCell>{getStatusBadge(caseItem.status)}</TableCell>
                          <TableCell>
                            {getDeadlineBadge(deadline.level, deadline.text)}
                          </TableCell>
                          <TableCell>
                            <div className="truncate max-w-[100px]">
                              {caseItem.agent?.name || '-'}
                            </div>
                          </TableCell>
                          <TableCell className="text-muted-foreground">
                            {new Date(caseItem.created_at).toLocaleDateString('zh-CN')}
                          </TableCell>
                        </TableRow>
                      )
                    })
                  )}
                </TableBody>
              </Table>
            </div>

            {/* 分页 */}
            {totalPages > 1 && (
              <div className="flex items-center justify-between">
                <div className="text-sm text-muted-foreground">
                  第 {(page - 1) * pageSize + 1} - {Math.min(page * pageSize, total)} 条，共 {total} 条
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setPage(page - 1)}
                    disabled={page <= 1}
                  >
                    上一页
                  </Button>
                  <div className="flex items-center gap-1">
                    {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                      let pageNum: number
                      if (totalPages <= 5) {
                        pageNum = i + 1
                      } else if (page <= 3) {
                        pageNum = i + 1
                      } else if (page >= totalPages - 2) {
                        pageNum = totalPages - 4 + i
                      } else {
                        pageNum = page - 2 + i
                      }
                      return (
                        <Button
                          key={pageNum}
                          variant={pageNum === page ? 'default' : 'outline'}
                          size="sm"
                          className="w-8"
                          onClick={() => setPage(pageNum)}
                        >
                          {pageNum}
                        </Button>
                      )
                    })}
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setPage(page + 1)}
                    disabled={page >= totalPages}
                  >
                    下一页
                  </Button>
                </div>
              </div>
            )}
          </div>
        }
        rightPanel={<CaseDetailPanel />}
        rightPanelOpen={isDetailOpen}
        onRightPanelClose={closeDetail}
        defaultLeftWidth={60}
        minLeftWidth={40}
        maxLeftWidth={75}
        rightPanelMinWidth={350}
      />

      {/* 案件表单弹窗 */}
      <CaseForm />
    </>
  )
}
