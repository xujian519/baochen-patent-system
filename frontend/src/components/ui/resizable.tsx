import { useState, useRef, useCallback, useEffect } from 'react'
import { cn } from '@/lib/utils'
import { PanelLeftClose, PanelLeft } from 'lucide-react'
import { Button } from '@/components/ui/button'

interface ResizablePanelsProps {
  leftPanel: React.ReactNode
  rightPanel: React.ReactNode
  rightPanelOpen: boolean
  onRightPanelClose: () => void
  defaultLeftWidth?: number // 百分比
  minLeftWidth?: number // 百分比
  maxLeftWidth?: number // 百分比
  rightPanelMinWidth?: number // 像素
}

export function ResizablePanels({
  leftPanel,
  rightPanel,
  rightPanelOpen,
  onRightPanelClose,
  defaultLeftWidth = 60,
  minLeftWidth = 30,
  maxLeftWidth = 80,
  rightPanelMinWidth = 300,
}: ResizablePanelsProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [leftWidth, setLeftWidth] = useState(defaultLeftWidth)
  const [isDragging, setIsDragging] = useState(false)

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleMouseMove = useCallback((e: MouseEvent) => {
    if (!isDragging || !containerRef.current) return

    const containerRect = containerRef.current.getBoundingClientRect()
    const containerWidth = containerRect.width
    const mouseX = e.clientX - containerRect.left

    // 计算右侧面板最小宽度对应的左面板最大宽度
    const effectiveMaxLeftWidth = Math.min(
      maxLeftWidth,
      ((containerWidth - rightPanelMinWidth) / containerWidth) * 100
    )

    // 计算新的左侧宽度百分比
    let newLeftWidth = (mouseX / containerWidth) * 100
    newLeftWidth = Math.max(minLeftWidth, Math.min(effectiveMaxLeftWidth, newLeftWidth))

    setLeftWidth(newLeftWidth)
  }, [isDragging, minLeftWidth, maxLeftWidth, rightPanelMinWidth])

  const handleMouseUp = useCallback(() => {
    setIsDragging(false)
  }, [])

  useEffect(() => {
    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)
      document.body.style.cursor = 'col-resize'
      document.body.style.userSelect = 'none'
    } else {
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
      document.body.style.cursor = ''
      document.body.style.userSelect = ''
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
      document.body.style.cursor = ''
      document.body.style.userSelect = ''
    }
  }, [isDragging, handleMouseMove, handleMouseUp])

  return (
    <div ref={containerRef} className="flex h-full w-full overflow-hidden">
      {/* 左侧面板 */}
      <div
        className={cn(
          'flex flex-col overflow-hidden transition-[width] duration-0',
          rightPanelOpen ? '' : 'w-full'
        )}
        style={{ width: rightPanelOpen ? `${leftWidth}%` : '100%' }}
      >
        {leftPanel}
      </div>

      {/* 分隔条 */}
      {rightPanelOpen && (
        <div
          className={cn(
            'group relative flex w-1.5 flex-shrink-0 items-center justify-center bg-border hover:bg-primary/50',
            isDragging && 'bg-primary'
          )}
          onMouseDown={handleMouseDown}
        >
          {/* 拖动手柄 */}
          <div
            className={cn(
              'absolute inset-y-0 -left-1 -right-1 cursor-col-resize',
              isDragging && 'bg-primary/20'
            )}
          />

          {/* 收起按钮 */}
          <Button
            variant="ghost"
            size="icon"
            className="absolute left-0 top-2 h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
            onClick={onRightPanelClose}
            title="关闭面板"
          >
            <PanelLeftClose className="h-4 w-4" />
          </Button>
        </div>
      )}

      {/* 右侧面板 */}
      {rightPanelOpen && (
        <div
          className="flex-shrink-0 overflow-hidden border-l bg-background"
          style={{ width: `${100 - leftWidth}%` }}
        >
          {rightPanel}
        </div>
      )}

      {/* 展开按钮（当右侧面板关闭时） */}
      {!rightPanelOpen && (
        <Button
          variant="ghost"
          size="icon"
          className="fixed right-4 top-20 z-10 h-8 w-8 shadow-md"
          onClick={() => onRightPanelClose()} // 这里应该调用打开方法，需要父组件处理
          title="展开面板"
        >
          <PanelLeft className="h-4 w-4" />
        </Button>
      )}
    </div>
  )
}
