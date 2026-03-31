import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User, LoginRequest, LoginResponse } from '@/types/api'
import client from '@/api/client'

/**
 * 统一提取 API 错误信息的工具函数
 */
function getErrorMessage(err: unknown, defaultMessage: string): string {
  if (err && typeof err === 'object') {
    const error = err as { response?: { data?: { detail?: string; message?: string } }; message?: string }
    return error.response?.data?.detail || error.response?.data?.message || error.message || defaultMessage
  }
  return defaultMessage
}

interface AuthState {
  token: string | null
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

interface AuthActions {
  login: (credentials: LoginRequest) => Promise<boolean>
  logout: () => void
  loadUser: () => Promise<void>
  setUser: (user: User) => void
  clearError: () => void
}

type AuthStore = AuthState & AuthActions

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      // 初始状态
      token: null,
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      // 登录
      login: async (credentials: LoginRequest) => {
        set({ isLoading: true, error: null })
        try {
          const response = (await client.post(
            '/api/v1/auth/login',
            credentials
          )) as LoginResponse
          localStorage.setItem('token', response.access_token)
          set({
            token: response.access_token,
            user: response.user,
            isAuthenticated: true,
            isLoading: false,
          })
          return true
        } catch (err) {
          set({ error: getErrorMessage(err, '登录失败，请检查邮箱和密码'), isLoading: false })
          return false
        }
      },

      // 退出登录
      logout: () => {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        set({
          token: null,
          user: null,
          isAuthenticated: false,
          error: null,
        })
      },

      // 加载当前用户信息
      loadUser: async () => {
        const token = get().token || localStorage.getItem('token')
        if (!token) {
          set({ isAuthenticated: false })
          return
        }
        try {
          const response = (await client.get('/api/v1/auth/me')) as {
            user: User
          }
          set({
            user: response.user,
            isAuthenticated: true,
            token,
          })
        } catch {
          // Token 无效，清除状态
          localStorage.removeItem('token')
          set({
            token: null,
            user: null,
            isAuthenticated: false,
          })
        }
      },

      // 设置用户
      setUser: (user: User) => {
        set({ user })
      },

      // 清除错误
      clearError: () => {
        set({ error: null })
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
