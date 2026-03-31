import axios, { type AxiosError, type AxiosInstance } from 'axios'
import type { ApiResponse } from '@/types/api'

// 创建 Axios 实例
// baseURL 留空，让 Nginx 代理 /api/ 到后端
const client: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器：自动注入 JWT Token
client.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器：统一错误处理 + 解包响应
client.interceptors.response.use(
  (response) => {
    const data = response.data
    // 如果是统一响应格式 {code, data, message}，解包到内层
    if (data && typeof data === 'object' && 'code' in data && 'data' in data) {
      return data.data
    }
    return data
  },
  (error: AxiosError<ApiResponse<unknown>>) => {
    // 401/403 未授权，跳转登录
    if (error.response?.status === 401 || error.response?.status === 403) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // 避免登录页循环跳转
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default client
