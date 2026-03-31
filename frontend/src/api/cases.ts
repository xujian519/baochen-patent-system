import client from './client'
import type {
  PaginatedResponse,
  Case,
  CaseCreate,
  CaseUpdate,
  CaseFilters,
} from '@/types/api'

// 获取案件列表
// client 已经在拦截器中解包了 data.data，直接返回的就是 PaginatedResponse<Case>
export async function getCases(params: CaseFilters & { page?: number; page_size?: number }) {
  return client.get('/api/v1/cases/', { params }) as Promise<PaginatedResponse<Case>>
}

// 获取单个案件详情
export async function getCase(id: number) {
  return client.get(`/api/v1/cases/${id}`) as Promise<Case>
}

// 创建案件
export async function createCase(data: CaseCreate) {
  return client.post('/api/v1/cases/', data) as Promise<Case>
}

// 更新案件
export async function updateCase(id: number, data: CaseUpdate) {
  return client.put(`/api/v1/cases/${id}`, data) as Promise<Case>
}

// 更新案件状态
export async function updateCaseStatus(id: number, status: string) {
  return client.patch(`/api/v1/cases/${id}/status`, { status }) as Promise<Case>
}

// 删除案件
export async function deleteCase(id: number) {
  return client.delete(`/api/v1/cases/${id}`) as Promise<void>
}
