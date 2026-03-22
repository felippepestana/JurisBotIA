'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
  LayoutDashboard,
  Briefcase,
  Users,
  FileText,
  Calendar,
  Scale,
  LogOut,
  Settings,
} from 'lucide-react'
import { cn } from '@/lib/utils'

const navItems = [
  { label: 'Dashboard', href: '/', icon: LayoutDashboard },
  { label: 'Casos', href: '/casos', icon: Briefcase },
  { label: 'Clientes', href: '/clientes', icon: Users },
  { label: 'Documentos', href: '/documentos', icon: FileText },
  { label: 'Prazos', href: '/prazos', icon: Calendar },
]

const bottomItems = [
  { label: 'Configurações', href: '/configuracoes', icon: Settings },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="flex h-screen w-64 flex-col border-r border-slate-200 bg-white">
      {/* Logo */}
      <div className="flex h-16 items-center gap-2 border-b border-slate-200 px-6">
        <Scale className="h-7 w-7 text-blue-700" />
        <span className="text-lg font-bold text-slate-900">JusBotAi</span>
      </div>

      {/* Navigation */}
      <nav className="flex flex-1 flex-col gap-1 overflow-y-auto p-4">
        <p className="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-slate-400">
          Menu Principal
        </p>
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.href

          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'sidebar-link',
                isActive && 'active'
              )}
            >
              <Icon className="h-4 w-4 shrink-0" />
              <span className="text-sm">{item.label}</span>
            </Link>
          )
        })}
      </nav>

      {/* Bottom section */}
      <div className="border-t border-slate-200 p-4">
        {bottomItems.map((item) => {
          const Icon = item.icon
          return (
            <Link key={item.href} href={item.href} className="sidebar-link">
              <Icon className="h-4 w-4 shrink-0" />
              <span className="text-sm">{item.label}</span>
            </Link>
          )
        })}
        <button className="sidebar-link mt-1 w-full text-left text-red-500 hover:bg-red-50 hover:text-red-600">
          <LogOut className="h-4 w-4 shrink-0" />
          <span className="text-sm">Sair</span>
        </button>
      </div>
    </aside>
  )
}
