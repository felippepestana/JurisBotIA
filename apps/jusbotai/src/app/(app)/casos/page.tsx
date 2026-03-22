import { Plus, Search, Filter } from 'lucide-react'
import { Header } from '@/components/layout/Header'
import { formatDate } from '@/lib/utils'

const cases = [
  {
    id: '1',
    number: '0001234-56.2024.8.26.0100',
    title: 'Ação de Indenização por Danos Morais',
    client: 'Maria Silva Santos',
    status: 'ativo',
    priority: 'alta',
    court: '1ª Vara Cível de São Paulo',
    openedAt: '2024-01-10',
    nextHearing: '2024-02-15',
  },
  {
    id: '2',
    number: '0009876-54.2024.8.26.0200',
    title: 'Divórcio Consensual',
    client: 'João Pedro Oliveira',
    status: 'aguardando',
    priority: 'media',
    court: '2ª Vara de Família de São Paulo',
    openedAt: '2024-01-15',
    nextHearing: '2024-02-20',
  },
  {
    id: '3',
    number: '0005432-10.2023.8.26.0050',
    title: 'Execução Trabalhista',
    client: 'Empresa ABC Ltda',
    status: 'ativo',
    priority: 'media',
    court: '3ª Vara do Trabalho de São Paulo',
    openedAt: '2023-11-05',
    nextHearing: '2024-02-22',
  },
  {
    id: '4',
    number: '0002345-67.2022.8.26.0300',
    title: 'Inventário e Partilha de Bens',
    client: 'Família Rodrigues',
    status: 'suspenso',
    priority: 'baixa',
    court: '1ª Vara de Sucessões de São Paulo',
    openedAt: '2022-08-20',
    nextHearing: undefined,
  },
  {
    id: '5',
    number: '0007654-32.2023.8.26.0400',
    title: 'Ação de Despejo por Falta de Pagamento',
    client: 'Carlos Eduardo Lima',
    status: 'encerrado',
    priority: 'alta',
    court: '5ª Vara Cível de São Paulo',
    openedAt: '2023-05-12',
    nextHearing: undefined,
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

const priorityLabels: Record<string, string> = {
  alta: 'Alta',
  media: 'Média',
  baixa: 'Baixa',
}

const priorityColors: Record<string, string> = {
  alta: 'badge-red',
  media: 'badge-yellow',
  baixa: 'badge-green',
}

export default function CasosPage() {
  return (
    <div className="p-6">
      <Header title="Casos" subtitle="Gerenciamento de processos judiciais" />

      {/* Actions bar */}
      <div className="mt-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex gap-2">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Buscar casos..."
              className="w-64 rounded-lg border border-slate-200 bg-white py-2 pl-9 pr-4 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>
          <button className="btn-secondary">
            <Filter className="h-4 w-4" />
            Filtros
          </button>
        </div>
        <button className="btn-primary">
          <Plus className="h-4 w-4" />
          Novo Caso
        </button>
      </div>

      {/* Cases table */}
      <div className="mt-4 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50">
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                  Processo
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                  Cliente
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                  Vara / Tribunal
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                  Prioridade
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                  Status
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                  Próx. Audiência
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                  Abertura
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {cases.map((caso) => (
                <tr key={caso.id} className="hover:bg-slate-50">
                  <td className="px-4 py-4">
                    <p className="font-medium text-slate-900">{caso.title}</p>
                    <p className="mt-0.5 font-mono text-xs text-slate-400">{caso.number}</p>
                  </td>
                  <td className="px-4 py-4 text-slate-600">{caso.client}</td>
                  <td className="px-4 py-4 text-slate-600">{caso.court}</td>
                  <td className="px-4 py-4">
                    <span className={priorityColors[caso.priority] ?? 'badge-slate'}>
                      {priorityLabels[caso.priority] ?? caso.priority}
                    </span>
                  </td>
                  <td className="px-4 py-4">
                    <span className={statusColors[caso.status] ?? 'badge-slate'}>
                      {statusLabels[caso.status] ?? caso.status}
                    </span>
                  </td>
                  <td className="px-4 py-4 text-slate-600">
                    {caso.nextHearing ? formatDate(caso.nextHearing) : '—'}
                  </td>
                  <td className="px-4 py-4 text-slate-600">{formatDate(caso.openedAt)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="flex items-center justify-between border-t border-slate-200 px-4 py-3">
          <p className="text-sm text-slate-500">
            Mostrando <span className="font-medium">1–{cases.length}</span> de{' '}
            <span className="font-medium">{cases.length}</span> casos
          </p>
          <div className="flex gap-2">
            <button className="btn-secondary py-1.5 text-xs" disabled>
              Anterior
            </button>
            <button className="btn-secondary py-1.5 text-xs" disabled>
              Próximo
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
