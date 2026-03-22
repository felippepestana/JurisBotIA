import { Plus, CheckCircle2, Circle, AlertTriangle } from 'lucide-react'
import { Header } from '@/components/layout/Header'
import { formatDate } from '@/lib/utils'

const deadlines = [
  {
    id: '1',
    title: 'Prazo para Contestação',
    description: 'Apresentar contestação no prazo legal de 15 dias',
    caseNumber: '0001234-56.2024.8.26.0100',
    client: 'Maria Silva Santos',
    dueDate: '2024-02-10',
    completed: false,
    urgent: true,
  },
  {
    id: '2',
    title: 'Audiência de Conciliação',
    description: 'Comparecer à audiência de conciliação designada pelo juízo',
    caseNumber: '0009876-54.2024.8.26.0200',
    client: 'João Pedro Oliveira',
    dueDate: '2024-02-15',
    completed: false,
    urgent: false,
  },
  {
    id: '3',
    title: 'Entrega de Documentos ao Perito',
    description: 'Apresentar documentos contábeis solicitados pelo perito judicial',
    caseNumber: '0005432-10.2023.8.26.0050',
    client: 'Empresa ABC Ltda',
    dueDate: '2024-02-18',
    completed: false,
    urgent: false,
  },
  {
    id: '4',
    title: 'Prazo para Recurso de Apelação',
    description: 'Interpor recurso de apelação contra sentença de primeiro grau',
    caseNumber: '0007654-32.2023.8.26.0400',
    client: 'Carlos Eduardo Lima',
    dueDate: '2024-02-25',
    completed: false,
    urgent: false,
  },
  {
    id: '5',
    title: 'Pagamento de Custas Processuais',
    description: 'Recolher guia de custas para distribuição do processo',
    caseNumber: '0003456-78.2024.8.26.0100',
    client: 'Ana Paula Ferreira',
    dueDate: '2024-02-08',
    completed: true,
    urgent: false,
  },
  {
    id: '6',
    title: 'Protocolo de Petição',
    description: 'Protocolar petição de juntada de documentos',
    caseNumber: '0001234-56.2024.8.26.0100',
    client: 'Maria Silva Santos',
    dueDate: '2024-02-05',
    completed: true,
    urgent: false,
  },
]

const pending = deadlines.filter((d) => !d.completed)
const completed = deadlines.filter((d) => d.completed)

export default function PrazosPage() {
  return (
    <div className="p-6">
      <Header title="Prazos" subtitle="Controle de prazos e audiências" />

      {/* Summary cards */}
      <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div className="rounded-xl border border-red-200 bg-red-50 p-4">
          <div className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-red-600" />
            <p className="font-semibold text-red-800">Urgentes</p>
          </div>
          <p className="mt-1 text-2xl font-bold text-red-700">
            {pending.filter((d) => d.urgent).length}
          </p>
          <p className="text-sm text-red-600">prazos críticos</p>
        </div>

        <div className="rounded-xl border border-yellow-200 bg-yellow-50 p-4">
          <div className="flex items-center gap-2">
            <Circle className="h-5 w-5 text-yellow-600" />
            <p className="font-semibold text-yellow-800">Pendentes</p>
          </div>
          <p className="mt-1 text-2xl font-bold text-yellow-700">{pending.length}</p>
          <p className="text-sm text-yellow-600">prazos em aberto</p>
        </div>

        <div className="rounded-xl border border-green-200 bg-green-50 p-4">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="h-5 w-5 text-green-600" />
            <p className="font-semibold text-green-800">Concluídos</p>
          </div>
          <p className="mt-1 text-2xl font-bold text-green-700">{completed.length}</p>
          <p className="text-sm text-green-600">prazos cumpridos</p>
        </div>
      </div>

      {/* Add deadline button */}
      <div className="mt-6 flex justify-end">
        <button className="btn-primary">
          <Plus className="h-4 w-4" />
          Novo Prazo
        </button>
      </div>

      {/* Pending deadlines */}
      <div className="mt-4">
        <h2 className="mb-3 text-base font-semibold text-slate-900">Prazos Pendentes</h2>
        <div className="space-y-3">
          {pending
            .sort((a, b) => new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime())
            .map((deadline) => (
              <div
                key={deadline.id}
                className={`rounded-xl border p-4 ${
                  deadline.urgent
                    ? 'border-red-200 bg-red-50'
                    : 'border-slate-200 bg-white'
                }`}
              >
                <div className="flex items-start gap-3">
                  <button
                    className="mt-0.5 shrink-0"
                    aria-label={`Marcar "${deadline.title}" como concluído`}
                  >
                    <Circle
                      className={`h-5 w-5 ${deadline.urgent ? 'text-red-400' : 'text-slate-300'}`}
                    />
                  </button>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <p className="font-medium text-slate-900">{deadline.title}</p>
                        <p className="mt-0.5 text-sm text-slate-500">{deadline.description}</p>
                        <p className="mt-1 font-mono text-xs text-slate-400">
                          {deadline.caseNumber}
                        </p>
                        <p className="text-xs text-slate-500">{deadline.client}</p>
                      </div>
                      <div className="shrink-0 text-right">
                        <p
                          className={`text-sm font-semibold ${
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
                  </div>
                </div>
              </div>
            ))}
        </div>
      </div>

      {/* Completed deadlines */}
      <div className="mt-6">
        <h2 className="mb-3 text-base font-semibold text-slate-900">Prazos Concluídos</h2>
        <div className="space-y-3">
          {completed.map((deadline) => (
            <div
              key={deadline.id}
              className="rounded-xl border border-slate-100 bg-slate-50 p-4 opacity-70"
            >
              <div className="flex items-start gap-3">
                <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-green-500" />
                <div className="min-w-0 flex-1">
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <p className="font-medium text-slate-600 line-through">{deadline.title}</p>
                      <p className="mt-0.5 text-sm text-slate-400">{deadline.description}</p>
                      <p className="mt-1 font-mono text-xs text-slate-400">
                        {deadline.caseNumber}
                      </p>
                    </div>
                    <p className="shrink-0 text-sm text-slate-400">{formatDate(deadline.dueDate)}</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
