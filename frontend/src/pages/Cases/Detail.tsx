import { useCaseStore } from '@/stores/case'
import { useAuthStore } from '@/stores/auth'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Edit, Trash2, X } from 'lucide-react'
import { useState } from 'react'

// 详情字段显示组件
function DetailField({
  label,
  value,
  className = '',
}: {
  label: string
  value?: string | null
  className?: string
}) {
  return (
    <div className={className}>
      <dt className="text-sm font-medium text-muted-foreground">{label}</dt>
      <dd className="mt-1 text-sm text-foreground">{value || '-'}</dd>
    </div>
  )
}

// 获取状态徽章样式
function getStatusBadge(status: string) {
  const statusStyles: Record<string, string> = {
    在审: 'bg-blue-100 text-blue-800',
    已授权: 'bg-green-100 text-green-800',
    已驳回: 'bg-red-100 text-red-800',
    已撤回: 'bg-gray-100 text-gray-800',
    已放弃: 'bg-gray-100 text-gray-600',
  }

  return (
    <Badge className={statusStyles[status] || 'bg-gray-100 text-gray-800'}>
      {status}
    </Badge>
  )
}

// 面板版本的案件详情（用于左右分栏布局）
export function CaseDetailPanel() {
  const {
    currentCase,
    isLoading,
    closeDetail,
    openForm,
    deleteCase,
  } = useCaseStore()

  const { user } = useAuthStore()
  const [isDeleting, setIsDeleting] = useState(false)

  // 处理删除
  const handleDelete = async () => {
    if (!currentCase || !confirm(`确定要删除案件 "${currentCase.case_number}" 吗？`)) {
      return
    }

    setIsDeleting(true)
    try {
      await deleteCase(currentCase.id)
    } catch {
      // 错误已在 store 中处理
    } finally {
      setIsDeleting(false)
    }
  }

  // 处理编辑
  const handleEdit = () => {
    if (currentCase) {
      openForm('edit', currentCase.id)
    }
  }

  if (!currentCase) {
    return (
      <div className="flex h-full items-center justify-center text-muted-foreground">
        <div className="text-center">
          <p className="text-lg">选择案件查看详情</p>
          <p className="text-sm mt-2">点击左侧列表中的案件行</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex h-full flex-col overflow-hidden">
      {/* 头部 */}
      <div className="flex-shrink-0 border-b p-4">
        <div className="flex items-start justify-between">
          <div className="flex-1 pr-4">
            <div className="flex items-center gap-2">
              <h2 className="text-lg font-semibold">{currentCase.case_number}</h2>
              {getStatusBadge(currentCase.status)}
            </div>
            <p className="mt-1 text-sm text-muted-foreground line-clamp-2">
              {currentCase.title}
            </p>
          </div>
          <Button variant="ghost" size="icon" onClick={closeDetail} className="flex-shrink-0">
            <X className="h-4 w-4" />
          </Button>
        </div>

        {/* 操作按钮 */}
        <div className="mt-4 flex gap-2">
          <Button variant="outline" size="sm" onClick={handleEdit}>
            <Edit className="mr-2 h-4 w-4" />
            编辑
          </Button>
          {user?.role === 'admin' && (
            <Button
              variant="destructive"
              size="sm"
              onClick={handleDelete}
              disabled={isDeleting}
            >
              <Trash2 className="mr-2 h-4 w-4" />
              删除
            </Button>
          )}
        </div>
      </div>

      {/* 内容区 */}
      {isLoading ? (
        <div className="flex flex-1 items-center justify-center">
          <div className="h-6 w-6 animate-spin rounded-full border-2 border-primary border-t-transparent" />
        </div>
      ) : (
        <div className="flex-1 overflow-y-auto p-4">
          <Tabs defaultValue="basic">
            <TabsList className="w-full grid grid-cols-6">
              <TabsTrigger value="basic">基本信息</TabsTrigger>
              <TabsTrigger value="timeline">时间线</TabsTrigger>
              <TabsTrigger value="files">文件</TabsTrigger>
              <TabsTrigger value="fees">费用</TabsTrigger>
              <TabsTrigger value="deadlines">期限</TabsTrigger>
              <TabsTrigger value="documents">官文</TabsTrigger>
            </TabsList>

            {/* 基本信息 Tab */}
            <TabsContent value="basic" className="mt-4 space-y-4">
              <dl className="grid grid-cols-2 gap-4">
                <DetailField label="案件编号" value={currentCase.case_number} />
                <DetailField label="主体" value={currentCase.entity} />
                <DetailField label="发明名称" value={currentCase.title} className="col-span-2" />
                <DetailField label="专利类型" value={currentCase.patent_type} />
                <DetailField label="当前阶段" value={currentCase.current_stage} />
                <DetailField label="申请号" value={currentCase.application_number} />
                <DetailField
                  label="申请日"
                  value={
                    currentCase.filing_date
                      ? new Date(currentCase.filing_date).toLocaleDateString('zh-CN')
                      : null
                  }
                />
                <DetailField
                  label="客户"
                  value={
                    currentCase.client
                      ? `${currentCase.client.name}${
                          currentCase.client.short_name
                            ? ` (${currentCase.client.short_name})`
                            : ''
                        }`
                      : null
                  }
                  className="col-span-2"
                />
                <DetailField label="代理师" value={currentCase.agent?.name} />
                <DetailField label="协办人" value={currentCase.assistant?.name} />
                <DetailField
                  label="最近期限"
                  value={
                    currentCase.nearest_deadline
                      ? new Date(currentCase.nearest_deadline).toLocaleDateString('zh-CN')
                      : null
                  }
                />
                <DetailField
                  label="创建时间"
                  value={new Date(currentCase.created_at).toLocaleString('zh-CN')}
                />
                <DetailField label="备注" value={currentCase.remarks} className="col-span-2" />
              </dl>
            </TabsContent>

            {/* 时间线 Tab */}
            <TabsContent value="timeline" className="mt-4">
              <div className="flex flex-col items-center justify-center py-12 text-muted-foreground">
                <p>时间线功能开发中...</p>
              </div>
            </TabsContent>

            {/* 文件 Tab */}
            <TabsContent value="files" className="mt-4">
              <div className="flex flex-col items-center justify-center py-12 text-muted-foreground">
                <p>文件管理功能开发中...</p>
              </div>
            </TabsContent>

            {/* 费用 Tab */}
            <TabsContent value="fees" className="mt-4">
              <div className="flex flex-col items-center justify-center py-12 text-muted-foreground">
                <p>费用管理功能开发中...</p>
              </div>
            </TabsContent>

            {/* 期限 Tab */}
            <TabsContent value="deadlines" className="mt-4">
              <div className="flex flex-col items-center justify-center py-12 text-muted-foreground">
                <p>期限管理功能开发中...</p>
              </div>
            </TabsContent>

            {/* 官文 Tab */}
            <TabsContent value="documents" className="mt-4">
              <div className="flex flex-col items-center justify-center py-12 text-muted-foreground">
                <p>官方来文功能开发中...</p>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      )}
    </div>
  )
}

// 默认导出（保持向后兼容，用于独立页面）
export default CaseDetailPanel
