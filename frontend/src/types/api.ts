// 统一 API 响应格式
export interface ApiResponse<T> {
  code: number
  data: T
  message: string
}

// 分页响应
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

// 用户
export interface User {
  id: number
  name: string
  role: 'admin' | 'agent' | 'staff'
  entity: string
  email: string
  phone: string
}

// 登录请求
export interface LoginRequest {
  email: string
  password: string
}

// 登录响应
export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

// 客户
export interface Client {
  id: number
  name: string
  short_name: string | null
  contact_person: string | null
  phone: string | null
  email: string | null
  type: '企业' | '个人'
  fee_reduction: boolean
  created_at: string
}

// 案件
export interface Case {
  id: number
  case_number: string
  entity: string
  client_id: number
  client?: Client
  title: string
  patent_type: '发明' | '实用新型' | '外观设计'
  application_number: string | null
  filing_date: string | null
  status: string
  current_stage: string | null
  agent_id: number | null
  agent?: User
  assistant_id: number | null
  assistant?: User
  nearest_deadline: string | null
  deadline_level: number
  remarks: string | null
  created_at: string
  updated_at: string
}

// 案件创建请求（支持 ID 或名称）
export interface CaseCreate {
  client_id?: number
  client_name?: string
  title: string
  patent_type: '发明' | '实用新型' | '外观设计'
  agent_id?: number | null
  agent_name?: string
  assistant_id?: number | null
  assistant_name?: string
  remarks?: string
}

// 案件更新请求
export interface CaseUpdate {
  title?: string
  patent_type?: '发明' | '实用新型' | '外观设计'
  application_number?: string | null
  filing_date?: string | null
  client_id?: number
  client_name?: string
  agent_id?: number | null
  agent_name?: string
  assistant_id?: number | null
  assistant_name?: string
  remarks?: string
  case_number?: string
}

// 案件筛选条件
export interface CaseFilters {
  search?: string
  status?: string
  patent_type?: string
  client_id?: number
  agent_id?: number
}

// 客户创建请求
export interface ClientCreate {
  name: string
  short_name?: string
  contact_person?: string
  phone?: string
  email?: string
  type: '企业' | '个人'
  fee_reduction?: boolean
}

// 客户更新请求
export interface ClientUpdate {
  name?: string
  short_name?: string
  contact_person?: string
  phone?: string
  email?: string
  type?: '企业' | '个人'
  fee_reduction?: boolean
}

// 费用
export interface Fee {
  id: number
  case_id: number
  client_id: number
  fee_type: string
  amount: number
  fee_date: string | null
  paid_date: string | null
  status: '未缴' | '已缴' | '减免' | '待确认'
}

// 期限
export interface Deadline {
  id: number
  case_id: number
  deadline_type: string
  deadline_date: string
  warning_level: number
  is_completed: boolean
  description: string | null
}

// 任务
export interface Task {
  id: number
  title: string
  task_type: string
  priority: '紧急' | '高' | '中' | '低'
  status: '待开始' | '进行中' | '待审核' | '已完成' | '已取消'
  assignee_id: number | null
  due_date: string | null
  progress: number
}
