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

// 导入共享模块
import {
  STAGE_FILTER_OPTIONS,
  CASE_STATUS_FILTER_OPTIONS,
  PATENT_TYPE_OPTIONS,
  getDaysRemaining,
  getFeeReductionLabel,
  StageBadge,
  CaseStatusBadge,
  DeadlineBadge,
  formatDate,
} from '@/utils/case-helpers'

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
  }, [fetchCases])

  // 搜索防抖处理
  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchInput !== filters.search) {
        setFilters({ search: searchInput })
      }
    }, 300)
    return () => clearTimeout(timer)
  }, [searchInput, filters.search, setFilters])

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
                  placeholder="搜索案件编号、案件名称、申请号..."
                  value={searchInput}
                  onChange={(e) => setSearchInput(e.target.value)}
                  className="pl-9"
                />
              </div>

              {/* 案件状态筛选 */}
              <Select
                value={filters.case_status || 'all'}
                onValueChange={(value) => setFilters({ case_status: value === 'all' ? '' : value })}
              >
                <SelectTrigger className="w-[120px]">
                  <SelectValue placeholder="状态" />
                </SelectTrigger>
                <SelectContent>
                  {CASE_STATUS_FILTER_OPTIONS.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      {option.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              {/* 案件阶段筛选 */}
              <Select
                value={filters.stage || 'all'}
                onValueChange={(value) => setFilters({ stage: value === 'all' ? '' : value })}
              >
                <SelectTrigger className="w-[120px]">
                  <SelectValue placeholder="阶段" />
                </SelectTrigger>
                <SelectContent>
                  {STAGE_FILTER_OPTIONS.map((option) => (
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
                    <TableHead className="w-[130px]">案件编号</TableHead>
                    <TableHead className="min-w-[180px]">案件名称</TableHead>
                    <TableHead className="w-[80px]">类型</TableHead>
                    <TableHead className="w-[120px]">申请号</TableHead>
                    <TableHead className="w-[100px]">客户</TableHead>
                    <TableHead className="w-[80px]">案件阶段</TableHead>
                    <TableHead className="w-[80px]">案件状态</TableHead>
                    <TableHead className="w-[60px]">费减</TableHead>
                    <TableHead className="w-[80px]">专利权人</TableHead>
                    <TableHead className="w-[90px]">立案日期</TableHead>
                    <TableHead className="w-[90px]">递交日期</TableHead>
                    <TableHead className="w-[90px]">授权日期</TableHead>
                    <TableHead className="w-[80px]">最近期限</TableHead>
                    <TableHead className="w-[80px]">代理师</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {isLoading ? (
                    <TableRow>
                      <TableCell colSpan={14} className="h-24 text-center">
                        <div className="flex items-center justify-center">
                          <div className="h-6 w-6 animate-spin rounded-full border-2 border-primary border-t-transparent" />
                          <span className="ml-2 text-muted-foreground">加载中...</span>
                        </div>
                      </TableCell>
                    </TableRow>
                  ) : cases.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={14} className="h-24 text-center text-muted-foreground">
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
                            <div className="truncate max-w-[200px]" title={caseItem.title}>
                              {caseItem.title}
                            </div>
                          </TableCell>
                          <TableCell>
                            <Badge variant="outline">{caseItem.patent_type}</Badge>
                          </TableCell>
                          <TableCell className="font-mono text-xs">
                            {caseItem.application_number || '-'}
                          </TableCell>
                          <TableCell>
                            <div className="truncate max-w-[100px]" title={caseItem.client?.name}>
                              {caseItem.client?.short_name || caseItem.client?.name || '-'}
                            </div>
                          </TableCell>
                          <TableCell><StageBadge stage={caseItem.stage} /></TableCell>
                          <TableCell><CaseStatusBadge caseStatus={caseItem.case_status} /></TableCell>
                          <TableCell className="text-center">
                            <span className="text-xs font-medium">
                              {getFeeReductionLabel(caseItem.fee_reduction_ratio || 0)}
                            </span>
                          </TableCell>
                          <TableCell>
                            <div className="truncate max-w-[80px]" title={caseItem.patent_holder || caseItem.client?.name}>
                              {caseItem.patent_holder || caseItem.client?.short_name || '-'}
                            </div>
                          </TableCell>
                          <TableCell className="text-muted-foreground text-xs">
                            {formatDate(caseItem.created_at)}
                          </TableCell>
                          <TableCell className="text-muted-foreground text-xs">
                            {formatDate(caseItem.filing_date)}
                          </TableCell>
                          <TableCell className="text-muted-foreground text-xs">
                            {formatDate(caseItem.grant_date)}
                          </TableCell>
                          <TableCell>
                            <DeadlineBadge daysText={deadline.text} level={deadline.level} />
                          </TableCell>
                          <TableCell>
                            <div className="truncate max-w-[80px]">
                              {caseItem.agent?.name || '-'}
                            </div>
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
        defaultLeftWidth={55}
        minLeftWidth={40}
        maxLeftWidth={70}
        rightPanelMinWidth={400}
      />

      {/* 案件表单弹窗 */}
      <CaseForm />
    </>
  )
}
