import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  Briefcase,
  Users,
  DollarSign,
  FileText,
  Calendar,
  Mail,
  CheckSquare,
  BarChart3,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { useState } from 'react'

// 导航菜单项
const navItems = [
  { path: '/dashboard', label: '仪表盘', icon: LayoutDashboard },
  { path: '/cases', label: '案件管理', icon: Briefcase },
  { path: '/clients', label: '客户管理', icon: Users },
  { path: '/fees', label: '费用管理', icon: DollarSign },
  { path: '/documents', label: '文件管理', icon: FileText },
  { path: '/deadlines', label: '期限日历', icon: Calendar },
  { path: '/letters', label: '官方来文', icon: Mail },
  { path: '/tasks', label: '任务管理', icon: CheckSquare },
  { path: '/reports', label: '统计报表', icon: BarChart3 },
]

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false)

  return (
    <aside
      className={cn(
        'flex h-full flex-col border-r bg-card transition-all duration-300',
        collapsed ? 'w-16' : 'w-56'
      )}
    >
      {/* Logo 区域 */}
      <div className="flex h-16 items-center justify-center border-b px-4">
        {!collapsed && (
          <span className="text-lg font-semibold text-primary">
            宝宸专利管理
          </span>
        )}
        {collapsed && (
          <span className="text-xl font-bold text-primary">宝</span>
        )}
      </div>

      {/* 导航菜单 */}
      <nav className="flex-1 space-y-1 p-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              cn(
                'flex items-center rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                'hover:bg-accent hover:text-accent-foreground',
                isActive
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground',
                collapsed && 'justify-center'
              )
            }
            title={collapsed ? item.label : undefined}
          >
            <item.icon className="h-5 w-5 shrink-0" />
            {!collapsed && <span className="ml-3">{item.label}</span>}
          </NavLink>
        ))}
      </nav>

      {/* 折叠按钮 */}
      <div className="border-t p-2">
        <button
          onClick={() => setCollapsed(!collapsed)}
          className={cn(
            'flex w-full items-center justify-center rounded-lg py-2 text-muted-foreground transition-colors',
            'hover:bg-accent hover:text-accent-foreground'
          )}
        >
          {collapsed ? (
            <ChevronRight className="h-5 w-5" />
          ) : (
            <>
              <ChevronLeft className="h-5 w-5" />
              <span className="ml-2 text-sm">收起</span>
            </>
          )}
        </button>
      </div>
    </aside>
  )
}
