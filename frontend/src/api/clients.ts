import client from './client'
import type {
  PaginatedResponse,
  Client,
  ClientCreate,
  ClientUpdate,
} from '@/types/api'

// 获取客户列表
export async function getClients(params?: { page?: number; page_size?: number; search?: string }) {
  return client.get('/api/v1/clients/', { params }) as Promise<PaginatedResponse<Client>>
}

// 获取所有客户（用于下拉选择，不分页）
export async function getAllClients(search?: string) {
  const result = client.get('/api/v1/clients/', {
    params: { page: 1, page_size: 1000, search },
  }) as Promise<PaginatedResponse<Client>>
  return result.then(r => r.items)
}

// 获取单个客户详情
export async function getClient(id: number) {
  return client.get(`/api/v1/clients/${id}`) as Promise<Client>
}

// 创建客户
export async function createClient(data: ClientCreate) {
  return client.post('/api/v1/clients/', data) as Promise<Client>
}

// 更新客户
export async function updateClient(id: number, data: ClientUpdate) {
  return client.put(`/api/v1/clients/${id}`, data) as Promise<Client>
}

// 删除客户
export async function deleteClient(id: number) {
  return client.delete(`/api/v1/clients/${id}`) as Promise<void>
}
