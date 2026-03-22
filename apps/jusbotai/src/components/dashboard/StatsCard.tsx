import { type LucideIcon } from 'lucide-react'
import { cn } from '@/lib/utils'

interface StatsCardProps {
  title: string
  value: string | number
  description?: string
  icon: LucideIcon
  trend?: {
    value: number
    label: string
    positive?: boolean
  }
  color?: 'blue' | 'green' | 'yellow' | 'red' | 'slate'
}

const colorMap = {
  blue: {
    icon: 'bg-blue-50 text-blue-700',
    border: 'border-blue-100',
  },
  green: {
    icon: 'bg-green-50 text-green-700',
    border: 'border-green-100',
  },
  yellow: {
    icon: 'bg-yellow-50 text-yellow-700',
    border: 'border-yellow-100',
  },
  red: {
    icon: 'bg-red-50 text-red-700',
    border: 'border-red-100',
  },
  slate: {
    icon: 'bg-slate-100 text-slate-600',
    border: 'border-slate-200',
  },
}

export function StatsCard({
  title,
  value,
  description,
  icon: Icon,
  trend,
  color = 'blue',
}: StatsCardProps) {
  const colors = colorMap[color]

  return (
    <div className="card">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">{title}</p>
          <p className="mt-1 text-3xl font-bold text-slate-900">{value}</p>
          {description && <p className="mt-1 text-sm text-slate-500">{description}</p>}
        </div>
        <div className={cn('rounded-lg p-2.5', colors.icon)}>
          <Icon className="h-5 w-5" />
        </div>
      </div>

      {trend && (
        <div className="mt-4 flex items-center gap-1.5">
          <span
            className={cn(
              'text-xs font-medium',
              trend.positive ? 'text-green-600' : 'text-red-600'
            )}
          >
            {trend.positive ? '+' : '-'}
            {Math.abs(trend.value)}%
          </span>
          <span className="text-xs text-slate-500">{trend.label}</span>
        </div>
      )}
    </div>
  )
}
