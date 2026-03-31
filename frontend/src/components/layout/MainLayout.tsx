import { useEffect } from 'react'
import { Outlet } from 'react-router-dom'
import { TooltipProvider } from '@/components/ui/tooltip'
import { Toaster } from '@/components/ui/sonner'
import { useAuthStore } from '@/stores/auth'
import Sidebar from './Sidebar'
import Header from './Header'

export default function MainLayout() {
  const { loadUser } = useAuthStore()

  // 应用启动时恢复用户状态
  useEffect(() => {
    loadUser()
  }, [loadUser])

  return (
    <TooltipProvider>
      <div className="flex h-screen bg-background">
        {/* 侧边栏 */}
        <Sidebar />

        {/* 主内容区 */}
        <div className="flex flex-1 flex-col overflow-hidden">
          {/* 顶部工具栏 */}
          <Header />

          {/* 页面内容 */}
          <main className="flex-1 overflow-auto p-6">
            <Outlet />
          </main>
        </div>
      </div>

      {/* 全局 Toast 提示 */}
      <Toaster position="top-right" />
    </TooltipProvider>
  )
}
