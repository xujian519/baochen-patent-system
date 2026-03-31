import { useEffect, useState } from 'react'
import { useCaseStore } from '@/stores/case'
import { useAuthStore } from '@/stores/auth'
import * as clientsApi from '@/api/clients'
import * as usersApi from '@/api/users'
import type { Client, User } from '@/types/api'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Combobox, type ComboboxOption } from '@/components/ui/combobox'
import { toast } from 'sonner'

// 专利类型选项
const PATENT_TYPES = [
  { value: '发明', label: '发明' },
  { value: '实用新型', label: '实用新型' },
  { value: '外观设计', label: '外观设计' },
]

export default function CaseForm() {
  const {
    isFormOpen,
    formMode,
    formCaseId,
    currentCase,
    isLoading,
    createCase,
    updateCase,
    closeForm,
  } = useCaseStore()

  const { user } = useAuthStore()

  // 下拉选项数据
  const [clients, setClients] = useState<Client[]>([])
  const [agents, setAgents] = useState<User[]>([])
  const [staffs, setStaffs] = useState<User[]>([])

  // 加载状态
  const [isLoadingOptions, setIsLoadingOptions] = useState(false)

  // 表单数据（支持 ID 和名称两种形式）
  const [formData, setFormData] = useState({
    client_value: '', // 可以是 ID（数字字符串）或名称
    title: '',
    patent_type: '发明',
    agent_value: '',
    assistant_value: '',
    application_number: '',
    filing_date: '',
    remarks: '',
    case_number: '',
  })

  // 表单错误
  const [errors, setErrors] = useState<Record<string, string>>({})

  // 加载下拉选项
  useEffect(() => {
    if (isFormOpen) {
      setIsLoadingOptions(true)
      Promise.all([clientsApi.getAllClients(), usersApi.getAgents(), usersApi.getStaff()])
        .then(([clientsData, agentsData, staffsData]) => {
          setClients(clientsData)
          setAgents(agentsData)
          setStaffs(staffsData)
        })
        .catch(() => {
          toast.error('加载选项数据失败')
        })
        .finally(() => {
          setIsLoadingOptions(false)
        })
    }
  }, [isFormOpen])

  // 编辑模式：初始化表单数据
  useEffect(() => {
    if (formMode === 'edit' && currentCase) {
      setFormData({
        client_value: currentCase.client?.name || String(currentCase.client_id),
        title: currentCase.title,
        patent_type: currentCase.patent_type,
        agent_value: currentCase.agent?.name || '',
        assistant_value: currentCase.assistant?.name || '',
        application_number: currentCase.application_number || '',
        filing_date: currentCase.filing_date ? currentCase.filing_date.split('T')[0] : '',
        remarks: currentCase.remarks || '',
        case_number: currentCase.case_number,
      })
    } else {
      // 新建模式：重置表单
      setFormData({
        client_value: '',
        title: '',
        patent_type: '发明',
        agent_value: '',
        assistant_value: '',
        application_number: '',
        filing_date: '',
        remarks: '',
        case_number: '',
      })
    }
    setErrors({})
  }, [formMode, currentCase, isFormOpen])

  // 客户选项（用于 Combobox）
  const clientOptions: ComboboxOption[] = clients.map((client) => ({
    value: String(client.id),
    label: client.short_name || client.name,
    description: client.short_name ? client.name : undefined,
  }))

  // 代理师选项（用于 Combobox）
  const agentOptions: ComboboxOption[] = agents.map((agent) => ({
    value: String(agent.id),
    label: agent.name,
  }))

  // 员工选项（用于 Combobox）
  const staffOptions: ComboboxOption[] = staffs.map((staff) => ({
    value: String(staff.id),
    label: staff.name,
  }))

  // 判断值是否为数字 ID
  const isIdValue = (value: string): boolean => {
    if (!value) return false
    return /^\d+$/.test(value)
  }

  // 验证表单
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    if (!formData.client_value.trim()) {
      newErrors.client_value = '请输入或选择客户'
    }
    if (!formData.title.trim()) {
      newErrors.title = '请输入发明名称'
    }
    if (!formData.patent_type) {
      newErrors.patent_type = '请选择专利类型'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  // 提交表单
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validateForm()) {
      return
    }

    try {
      // 构建请求数据
      const getClientData = () => {
        if (isIdValue(formData.client_value)) {
          return { client_id: Number(formData.client_value) }
        }
        return { client_name: formData.client_value.trim() }
      }

      const getAgentData = () => {
        if (!formData.agent_value.trim()) return {}
        if (isIdValue(formData.agent_value)) {
          return { agent_id: Number(formData.agent_value) }
        }
        return { agent_name: formData.agent_value.trim() }
      }

      const getAssistantData = () => {
        if (!formData.assistant_value.trim()) return {}
        if (isIdValue(formData.assistant_value)) {
          return { assistant_id: Number(formData.assistant_value) }
        }
        return { assistant_name: formData.assistant_value.trim() }
      }

      if (formMode === 'create') {
        await createCase({
          ...getClientData(),
          title: formData.title.trim(),
          patent_type: formData.patent_type as '发明' | '实用新型' | '外观设计',
          ...getAgentData(),
          ...getAssistantData(),
          remarks: formData.remarks.trim() || undefined,
        })
        toast.success('案件创建成功')
      } else {
        if (!formCaseId) return

        await updateCase(formCaseId, {
          title: formData.title.trim(),
          patent_type: formData.patent_type as '发明' | '实用新型' | '外观设计',
          ...getAgentData(),
          ...getAssistantData(),
          application_number: formData.application_number.trim() || null,
          filing_date: formData.filing_date || null,
          remarks: formData.remarks.trim() || undefined,
          case_number: formData.case_number || undefined,
        })
        toast.success('案件更新成功')
      }
      closeForm()
    } catch {
      toast.error(formMode === 'create' ? '创建案件失败' : '更新案件失败')
    }
  }

  // 更新表单字段
  const updateField = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
    if (errors[field]) {
      setErrors((prev) => {
        const newErrors = { ...prev }
        delete newErrors[field]
        return newErrors
      })
    }
  }

  return (
    <Dialog open={isFormOpen} onOpenChange={(open) => !open && closeForm()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>
            {formMode === 'create' ? '新建案件' : '编辑案件'}
          </DialogTitle>
          <DialogDescription>
            {formMode === 'create'
              ? '填写案件基本信息，创建新的专利申请案件。'
              : '修改案件的基本信息。'}
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* 案件编号（编辑模式显示） */}
          {formMode === 'edit' && (
            <div className="space-y-2">
              <Label htmlFor="case_number">案件编号</Label>
              <Input
                id="case_number"
                value={formData.case_number}
                onChange={(e) => updateField('case_number', e.target.value)}
                placeholder="系统自动生成"
                disabled={user?.role !== 'admin'}
                className="font-mono"
              />
              {user?.role !== 'admin' && (
                <p className="text-xs text-muted-foreground">
                  案件编号仅管理员可修改
                </p>
              )}
            </div>
          )}

          {/* 客户（可输入/可选择） */}
          <div className="space-y-2">
            <Label htmlFor="client_value">
              客户 <span className="text-destructive">*</span>
            </Label>
            <Combobox
              options={clientOptions}
              value={formData.client_value}
              onChange={(value) => updateField('client_value', value)}
              placeholder="输入或选择客户..."
              emptyText="无匹配客户，按回车使用输入值"
              disabled={isLoadingOptions || formMode === 'edit'}
              allowCustom={true}
            />
            {errors.client_value && (
              <p className="text-xs text-destructive">{errors.client_value}</p>
            )}
            {formMode === 'edit' && (
              <p className="text-xs text-muted-foreground">
                客户不可修改
              </p>
            )}
          </div>

          {/* 发明名称 */}
          <div className="space-y-2">
            <Label htmlFor="title">
              发明名称 <span className="text-destructive">*</span>
            </Label>
            <Input
              id="title"
              value={formData.title}
              onChange={(e) => updateField('title', e.target.value)}
              placeholder="输入发明名称"
            />
            {errors.title && (
              <p className="text-xs text-destructive">{errors.title}</p>
            )}
          </div>

          {/* 专利类型 */}
          <div className="space-y-2">
            <Label htmlFor="patent_type">
              专利类型 <span className="text-destructive">*</span>
            </Label>
            <Select
              value={formData.patent_type}
              onValueChange={(value) => updateField('patent_type', value)}
            >
              <SelectTrigger id="patent_type">
                <SelectValue placeholder="选择专利类型" />
              </SelectTrigger>
              <SelectContent>
                {PATENT_TYPES.map((type) => (
                  <SelectItem key={type.value} value={type.value}>
                    {type.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {errors.patent_type && (
              <p className="text-xs text-destructive">{errors.patent_type}</p>
            )}
          </div>

          {/* 申请号和申请日（编辑模式显示） */}
          {formMode === 'edit' && (
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="application_number">申请号</Label>
                <Input
                  id="application_number"
                  value={formData.application_number}
                  onChange={(e) => updateField('application_number', e.target.value)}
                  placeholder="申请号"
                  className="font-mono"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="filing_date">申请日</Label>
                <Input
                  id="filing_date"
                  type="date"
                  value={formData.filing_date}
                  onChange={(e) => updateField('filing_date', e.target.value)}
                />
              </div>
            </div>
          )}

          {/* 代理师（可输入/可选择） */}
          <div className="space-y-2">
            <Label htmlFor="agent_value">代理师</Label>
            <Combobox
              options={agentOptions}
              value={formData.agent_value}
              onChange={(value) => updateField('agent_value', value)}
              placeholder="输入或选择代理师..."
              emptyText="无匹配代理师，按回车使用输入值"
              disabled={isLoadingOptions}
              allowCustom={true}
            />
          </div>

          {/* 协办人（可输入/可选择） */}
          <div className="space-y-2">
            <Label htmlFor="assistant_value">协办人</Label>
            <Combobox
              options={staffOptions}
              value={formData.assistant_value}
              onChange={(value) => updateField('assistant_value', value)}
              placeholder="输入或选择协办人..."
              emptyText="无匹配员工，按回车使用输入值"
              disabled={isLoadingOptions}
              allowCustom={true}
            />
          </div>

          {/* 备注 */}
          <div className="space-y-2">
            <Label htmlFor="remarks">备注</Label>
            <Input
              id="remarks"
              value={formData.remarks}
              onChange={(e) => updateField('remarks', e.target.value)}
              placeholder="备注信息（可选）"
            />
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={closeForm}>
              取消
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? (
                <>
                  <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent" />
                  处理中...
                </>
              ) : formMode === 'create' ? (
                '创建'
              ) : (
                '保存'
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
