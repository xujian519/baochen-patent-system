import { create } from 'zustand'
import type { Case, CaseFilters, CaseCreate, CaseUpdate } from '@/types/api'
import * as casesApi from '@/api/cases'

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

interface CaseState {
  // 状态
  cases: Case[]
  currentCase: Case | null
  total: number
  page: number
  pageSize: number
  isLoading: boolean
  error: string | null
  filters: CaseFilters

  // 详情抽屉状态
  isDetailOpen: boolean
  detailCaseId: number | null

  // 表单弹窗状态
  isFormOpen: boolean
  formMode: 'create' | 'edit'
  formCaseId: number | null

  // Actions
  fetchCases: (params?: CaseFilters & { page?: number; page_size?: number }) => Promise<void>
  fetchCase: (id: number) => Promise<void>
  createCase: (data: CaseCreate) => Promise<Case>
  updateCase: (id: number, data: CaseUpdate) => Promise<Case>
  deleteCase: (id: number) => Promise<void>
  setFilters: (filters: Partial<CaseFilters>) => void
  resetFilters: () => void
  setPage: (page: number) => void
  openDetail: (id: number) => void
  closeDetail: () => void
  openForm: (mode: 'create' | 'edit', id?: number) => void
  closeForm: () => void
  clearError: () => void
}

const defaultFilters: CaseFilters = {
  search: '',
  status: '',
  patent_type: '',
  client_id: undefined,
  agent_id: undefined,
}

export const useCaseStore = create<CaseState>((set, get) => ({
  // 初始状态
  cases: [],
  currentCase: null,
  total: 0,
  page: 1,
  pageSize: 20,
  isLoading: false,
  error: null,
  filters: defaultFilters,

  isDetailOpen: false,
  detailCaseId: null,

  isFormOpen: false,
  formMode: 'create',
  formCaseId: null,

  // 获取案件列表
  fetchCases: async (params) => {
    set({ isLoading: true, error: null })
    try {
      const { page, pageSize, filters } = get()
      const mergedParams = {
        page: params?.page ?? page,
        page_size: params?.page_size ?? pageSize,
        ...filters,
        ...params,
      }
      const data = await casesApi.getCases(mergedParams)
      set({
        cases: data.items,
        total: data.total,
        page: mergedParams.page,
        pageSize: mergedParams.page_size,
        isLoading: false,
      })
    } catch (err) {
      set({ error: getErrorMessage(err, '获取案件列表失败'), isLoading: false })
    }
  },

  // 获取单个案件详情
  fetchCase: async (id: number) => {
    set({ isLoading: true, error: null })
    try {
      const caseData = await casesApi.getCase(id)
      set({ currentCase: caseData, isLoading: false })
    } catch (err) {
      set({ error: getErrorMessage(err, '获取案件详情失败'), isLoading: false })
    }
  },

  // 创建案件
  createCase: async (data: CaseCreate) => {
    set({ isLoading: true, error: null })
    try {
      const newCase = await casesApi.createCase(data)
      // 刷新列表
      get().fetchCases()
      return newCase
    } catch (err) {
      set({ error: getErrorMessage(err, '创建案件失败'), isLoading: false })
      throw err
    }
  },

  // 更新案件
  updateCase: async (id: number, data: CaseUpdate) => {
    set({ isLoading: true, error: null })
    try {
      const updatedCase = await casesApi.updateCase(id, data)
      // 更新当前案件
      set({ currentCase: updatedCase, isLoading: false })
      // 刷新列表
      get().fetchCases()
      return updatedCase
    } catch (err) {
      set({ error: getErrorMessage(err, '更新案件失败'), isLoading: false })
      throw err
    }
  },

  // 删除案件
  deleteCase: async (id: number) => {
    set({ isLoading: true, error: null })
    try {
      await casesApi.deleteCase(id)
      // 关闭详情
      get().closeDetail()
      // 刷新列表
      get().fetchCases()
    } catch (err) {
      set({ error: getErrorMessage(err, '删除案件失败'), isLoading: false })
      throw err
    }
  },

  // 设置筛选条件
  setFilters: (filters: Partial<CaseFilters>) => {
    set((state) => ({
      filters: { ...state.filters, ...filters },
      page: 1, // 筛选条件改变时重置页码
    }))
    get().fetchCases()
  },

  // 重置筛选条件
  resetFilters: () => {
    set({ filters: defaultFilters, page: 1 })
    get().fetchCases()
  },

  // 设置页码
  setPage: (page: number) => {
    set({ page })
    get().fetchCases({ page })
  },

  // 打开详情抽屉
  openDetail: (id: number) => {
    set({ isDetailOpen: true, detailCaseId: id })
    get().fetchCase(id)
  },

  // 关闭详情抽屉
  closeDetail: () => {
    set({ isDetailOpen: false, detailCaseId: null, currentCase: null })
  },

  // 打开表单弹窗
  openForm: (mode: 'create' | 'edit', id?: number) => {
    set({
      isFormOpen: true,
      formMode: mode,
      formCaseId: id ?? null,
    })
    if (mode === 'edit' && id) {
      get().fetchCase(id)
    }
  },

  // 关闭表单弹窗
  closeForm: () => {
    set({
      isFormOpen: false,
      formMode: 'create',
      formCaseId: null,
    })
  },

  // 清除错误
  clearError: () => {
    set({ error: null })
  },
}))
