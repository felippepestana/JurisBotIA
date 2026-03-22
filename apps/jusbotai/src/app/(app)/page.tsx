import { Briefcase, Users, Calendar, FileText, ArrowRight, AlertCircle } from 'lucide-react'
import Link from 'next/link'
import { Header } from '@/components/layout/Header'
import { StatsCard } from '@/components/dashboard/StatsCard'
import { formatDate } from '@/lib/utils'

// Mock data for initial UI demonstration
const stats = {
  activeCases: 24,
  totalClients: 87,
  pendingDeadlines: 6,
  documentsGenerated: 142,
}

const recentCases = [
  {
    id: '1',
    number: '0001234-56.2024.8.26.0100',
    title: 'Ação de Indenização por Danos Morais',
    client: 'Maria Silva Santos',
    status: 'ativo',
    nextHearing: '2024-02-15',
  },
  {
    id: '2',
    number: '0009876-54.2024.8.26.0200',
    title: 'Divórcio Consensual',
    client: 'João Pedro Oliveira',
    status: 'aguardando',
    nextHearing: '2024-02-20',
  },
  {
    id: '3',
    number: '0005432-10.2023.8.26.0050',
    title: 'Execução Trabalhista',
    client: 'Empresa ABC Ltda',
    status: 'ativo',
    nextHearing: '2024-02-22',
  },
]

const upcomingDeadlines = [
  {
    id: '1',
    title: 'Prazo para Contestação',
    caseNumber: '0001234-56.2024.8.26.0100',
    dueDate: '2024-02-10',
    urgent: true,
  },
  {
    id: '2',
    title: 'Audiência de Conciliação',
    caseNumber: '0009876-54.2024.8.26.0200',
    dueDate: '2024-02-15',
    urgent: false,
  },
  {
    id: '3',
    title: 'Entrega de Documentos',
    caseNumber: '0005432-10.2023.8.26.0050',
    dueDate: '2024-02-18',
    urgent: false,
  },
]

const statusLabels: Record<string, string> = {
  ativo: 'Ativo',
  encerrado: 'Encerrado',
  suspenso: 'Suspenso',
  aguardando: 'Aguardando',
}

const statusColors: Record<string, string> = {
  ativo: 'badge-green',
  encerrado: 'badge-slate',
  suspenso: 'badge-yellow',
  aguardando: 'badge-blue',
}

export default function DashboardPage() {
  return (
    <div className="p-6">
      <Header
        title="Dashboard"
        subtitle="Bem-vindo de volta! Aqui está um resumo do seu escritório."
      />

      {/* Stats Grid */}
      <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatsCard
          title="Casos Ativos"
          value={stats.activeCases}
          description="Processos em andamento"
          icon={Briefcase}
          color="blue"
          trend={{ value: 12, label: 'vs. mês anterior', positive: true }}
        />
        <StatsCard
          title="Clientes"
          value={stats.totalClients}
          description="Total de clientes cadastrados"
          icon={Users}
          color="green"
          trend={{ value: 8, label: 'novos este mês', positive: true }}
        />
        <StatsCard
          title="Prazos Pendentes"
          value={stats.pendingDeadlines}
          description="Nos próximos 7 dias"
          icon={Calendar}
          color="yellow"
        />
        <StatsCard
          title="Documentos"
          value={stats.documentsGenerated}
          description="Documentos gerados"
          icon={FileText}
          color="slate"
        />
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Recent Cases */}
        <div className="card">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-base font-semibold text-slate-900">Casos Recentes</h2>
            <Link
              href="/casos"
              className="flex items-center gap-1 text-sm text-blue-600 hover:text-blue-700"
            >
              Ver todos
              <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>

          <div className="space-y-3">
            {recentCases.map((caso) => (
              <div
                key={caso.id}
                className="flex items-start justify-between rounded-lg border border-slate-100 p-3 hover:bg-slate-50"
              >
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-medium text-slate-900">{caso.title}</p>
                  <p className="mt-0.5 text-xs text-slate-500">{caso.client}</p>
                  <p className="mt-0.5 font-mono text-xs text-slate-400">{caso.number}</p>
                </div>
                <div className="ml-3 shrink-0 text-right">
                  <span className={statusColors[caso.status] ?? 'badge-slate'}>
                    {statusLabels[caso.status] ?? caso.status}
                  </span>
                  {caso.nextHearing && (
                    <p className="mt-1 text-xs text-slate-400">
                      Audiência: {formatDate(caso.nextHearing)}
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Upcoming Deadlines */}
        <div className="card">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-base font-semibold text-slate-900">Próximos Prazos</h2>
            <Link
              href="/prazos"
              className="flex items-center gap-1 text-sm text-blue-600 hover:text-blue-700"
            >
              Ver todos
              <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>

          <div className="space-y-3">
            {upcomingDeadlines.map((deadline) => (
              <div
                key={deadline.id}
                className="flex items-start gap-3 rounded-lg border border-slate-100 p-3 hover:bg-slate-50"
              >
                <div
                  className={`mt-0.5 shrink-0 rounded-full p-1 ${
                    deadline.urgent ? 'bg-red-100 text-red-600' : 'bg-slate-100 text-slate-500'
                  }`}
                >
                  <AlertCircle className="h-3.5 w-3.5" />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-slate-900">{deadline.title}</p>
                  <p className="mt-0.5 font-mono text-xs text-slate-400">{deadline.caseNumber}</p>
                </div>
                <div className="shrink-0 text-right">
                  <p
                    className={`text-sm font-medium ${
                      deadline.urgent ? 'text-red-600' : 'text-slate-700'
                    }`}
                  >
                    {formatDate(deadline.dueDate)}
                  </p>
                  {deadline.urgent && (
                    <span className="badge-red mt-1 inline-flex">Urgente</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
