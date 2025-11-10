/**
 * Componente Loading reutilizável
 */
import React from 'react'
import { cn } from '@/lib/utils'

export interface LoadingProps {
  size?: 'sm' | 'md' | 'lg' | 'xl'
  variant?: 'spinner' | 'dots' | 'pulse'
  text?: string
  fullScreen?: boolean
  className?: string
}

export const Loading: React.FC<LoadingProps> = ({
  size = 'md',
  variant = 'spinner',
  text,
  fullScreen = false,
  className,
}) => {
  const sizeMap = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16',
  }

  const Spinner = () => (
    <svg
      className={cn('animate-spin', sizeMap[size])}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
  )

  const Dots = () => (
    <div className="flex space-x-2">
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          className={cn(
            'rounded-full bg-current animate-pulse',
            sizeMap[size]
          )}
          style={{ animationDelay: `${i * 0.15}s` }}
        />
      ))}
    </div>
  )

  const Pulse = () => (
    <div
      className={cn(
        'rounded-full bg-primary-500 animate-pulse',
        sizeMap[size]
      )}
    />
  )

  const LoadingContent = () => (
    <div className={cn('flex flex-col items-center justify-center gap-3', className)}>
      {variant === 'spinner' && <Spinner />}
      {variant === 'dots' && <Dots />}
      {variant === 'pulse' && <Pulse />}
      {text && <p className="text-sm text-gray-600 animate-pulse">{text}</p>}
    </div>
  )

  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-white/80 backdrop-blur-sm flex items-center justify-center z-50">
        <LoadingContent />
      </div>
    )
  }

  return <LoadingContent />
}

Loading.displayName = 'Loading'
