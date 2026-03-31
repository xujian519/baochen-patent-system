import client from './client'
import type { User } from '@/types/api'

// 获取所有用户（用于下拉选择代理师和协办人）
export async function getUsers(role?: 'admin' | 'agent' | 'staff') {
  return client.get('/api/v1/users', {
    params: role ? { role } : {},
  }) as Promise<User[]>
}

// 获取代理师列表
export async function getAgents() {
  return getUsers('agent')
}

// 获取员工列表
export async function getStaff() {
  return getUsers('staff')
}
