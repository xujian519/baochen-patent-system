import { useState, useRef, useEffect } from 'react'
import { Check, ChevronsUpDown } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'

export interface ComboboxOption {
  value: string
  label: string
  description?: string
}

interface ComboboxProps {
  options: ComboboxOption[]
  value: string
  onChange: (value: string) => void
  placeholder?: string
  emptyText?: string
  disabled?: boolean
  className?: string
  allowCustom?: boolean // 是否允许自定义输入
}

export function Combobox({
  options,
  value,
  onChange,
  placeholder = '请选择...',
  emptyText = '无匹配项',
  disabled = false,
  className,
  allowCustom = true,
}: ComboboxProps) {
  const [open, setOpen] = useState(false)
  const [inputValue, setInputValue] = useState('')
  const inputRef = useRef<HTMLInputElement>(null)

  // 同步外部 value 到内部 inputValue
  useEffect(() => {
    if (value) {
      // 尝试从选项中找到对应的 label
      const option = options.find((opt) => opt.value === value)
      setInputValue(option ? option.label : value)
    } else {
      setInputValue('')
    }
  }, [value, options])

  // 过滤选项
  const filteredOptions = options.filter((option) =>
    option.label.toLowerCase().includes(inputValue.toLowerCase())
  )

  // 处理输入变化
  const handleInputChange = (newValue: string) => {
    setInputValue(newValue)
    // 如果允许自定义输入，实时更新 value
    if (allowCustom) {
      onChange(newValue)
    }
    // 自动打开下拉
    if (!open && newValue) {
      setOpen(true)
    }
  }

  // 处理选择
  const handleSelect = (selectedValue: string) => {
    const option = options.find((opt) => opt.value === selectedValue)
    if (option) {
      onChange(option.value)
      setInputValue(option.label)
    }
    setOpen(false)
  }

  // 失焦时处理
  const handleBlur = () => {
    // 延迟关闭，让点击事件有机会触发
    setTimeout(() => {
      setOpen(false)
      // 如果输入值不为空，但不在选项中，保持输入值
      if (inputValue && allowCustom) {
        onChange(inputValue)
      }
    }, 200)
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <div className={cn('relative', className)}>
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => handleInputChange(e.target.value)}
            onFocus={() => setOpen(true)}
            onBlur={handleBlur}
            placeholder={placeholder}
            disabled={disabled}
            className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
          />
          <Button
            type="button"
            variant="ghost"
            size="sm"
            className="absolute right-0 top-0 h-full px-3 hover:bg-transparent"
            onClick={() => setOpen(!open)}
            disabled={disabled}
          >
            <ChevronsUpDown className="h-4 w-4 opacity-50" />
          </Button>
        </div>
      </PopoverTrigger>
      <PopoverContent
        className="w-[--radix-popover-trigger-width] p-0"
        align="start"
        onOpenAutoFocus={(e) => e.preventDefault()}
      >
        <Command shouldFilter={false}>
          <CommandInput
            placeholder="搜索..."
            value={inputValue}
            onValueChange={handleInputChange}
          />
          <CommandList>
            {filteredOptions.length === 0 ? (
              allowCustom && inputValue ? (
                <CommandGroup>
                  <CommandItem
                    value={inputValue}
                    onSelect={() => {
                      onChange(inputValue)
                      setOpen(false)
                    }}
                  >
                    <Check className="mr-2 h-4 w-4 opacity-0" />
                    使用 "{inputValue}"
                  </CommandItem>
                </CommandGroup>
              ) : (
                <CommandEmpty>{emptyText}</CommandEmpty>
              )
            ) : (
              <CommandGroup>
                {filteredOptions.map((option) => (
                  <CommandItem
                    key={option.value}
                    value={option.value}
                    onSelect={() => handleSelect(option.value)}
                  >
                    <Check
                      className={cn(
                        'mr-2 h-4 w-4',
                        value === option.value ? 'opacity-100' : 'opacity-0'
                      )}
                    />
                    <div>
                      <div>{option.label}</div>
                      {option.description && (
                        <div className="text-xs text-muted-foreground">
                          {option.description}
                        </div>
                      )}
                    </div>
                  </CommandItem>
                ))}
              </CommandGroup>
            )}
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
