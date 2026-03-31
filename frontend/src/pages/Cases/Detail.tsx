import { useCaseStore } from '@/stores/case'
import { useAuthStore } from '@/stores/auth'
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
} from '@/components/ui/sheet'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Separator } from '@/components/ui/separator'
import { Edit, Trash2 } from 'lucide-react'
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

export default function CaseDetail() {
  const {
    currentCase,
    isDetailOpen,
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
      closeDetail()
      openForm('edit', currentCase.id)
    }
  }

  if (!currentCase) return null

  return (
    <Sheet open={isDetailOpen} onOpenChange={(open) => !open && closeDetail()}>
      <SheetContent className="w-[600px] sm:max-w-[600px] overflow-y-auto">
        <SheetHeader>
          <div className="flex items-center justify-between pr-8">
            <div>
              <SheetTitle className="flex items-center gap-2">
                {currentCase.case_number}
                {getStatusBadge(currentCase.status)}
              </SheetTitle>
              <SheetDescription className="mt-1">
                {currentCase.title}
              </SheetDescription>
            </div>
          </div>
        </SheetHeader>

        {isLoading ? (
          <div className="flex items-center justify-center py-8">
            <div className="h-6 w-6 animate-spin rounded-full border-2 border-primary border-t-transparent" />
          </div>
        ) : (
          <>
            {/* 操作按钮 */}
            <div className="flex gap-2 py-4">
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

            <Separator className="my-2" />

            {/* Tab 页内容 */}
            <Tabs defaultValue="basic" className="mt-4">
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
          </>
        )}
      </SheetContent>
    </Sheet>
  )
}
