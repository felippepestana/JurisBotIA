import { Plus, Search, Mail, Phone } from 'lucide-react'
import { Header } from '@/components/layout/Header'
import { formatDate, formatCPF, formatPhone } from '@/lib/utils'

const clients = [
  {
    id: '1',
    name: 'Maria Silva Santos',
    email: 'maria.santos@email.com',
    phone: '11987654321',
    cpf: '12345678901',
    city: 'São Paulo',
    state: 'SP',
    activeCases: 2,
    createdAt: '2023-06-15',
  },
  {
    id: '2',
    name: 'João Pedro Oliveira',
    email: 'joao.oliveira@email.com',
    phone: '11976543210',
    cpf: '98765432100',
    city: 'São Paulo',
    state: 'SP',
    activeCases: 1,
    createdAt: '2023-08-22',
  },
  {
    id: '3',
    name: 'Empresa ABC Ltda',
    email: 'juridico@empresaabc.com.br',
    phone: '1133334444',
    cpf: undefined,
    city: 'São Paulo',
    state: 'SP',
    activeCases: 1,
    createdAt: '2023-04-10',
  },
  {
    id: '4',
    name: 'Carlos Eduardo Lima',
    email: 'carlos.lima@email.com',
    phone: '11965432109',
    cpf: '45678901234',
    city: 'Santo André',
    state: 'SP',
    activeCases: 0,
    createdAt: '2022-11-30',
  },
  {
    id: '5',
    name: 'Ana Paula Ferreira',
    email: 'ana.ferreira@email.com',
    phone: '11954321098',
    cpf: '56789012345',
    city: 'Guarulhos',
    state: 'SP',
    activeCases: 1,
    createdAt: '2024-01-08',
  },
]

export default function ClientesPage() {
  return (
    <div className="p-6">
      <Header title="Clientes" subtitle="Gestão de clientes do escritório" />

      {/* Actions bar */}
      <div className="mt-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Buscar clientes..."
            className="w-72 rounded-lg border border-slate-200 bg-white py-2 pl-9 pr-4 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </div>
        <button className="btn-primary">
          <Plus className="h-4 w-4" />
          Novo Cliente
        </button>
      </div>

      {/* Clients grid */}
      <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {clients.map((client) => (
          <div
            key={client.id}
            className="card cursor-pointer transition-shadow hover:shadow-md"
          >
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 text-sm font-semibold text-blue-700">
                  {client.name
                    .split(' ')
                    .map((n) => n[0])
                    .slice(0, 2)
                    .join('')}
                </div>
                <div>
                  <p className="font-semibold text-slate-900">{client.name}</p>
                  <p className="text-xs text-slate-500">
                    {client.city}, {client.state}
                  </p>
                </div>
              </div>
              <span
                className={`badge ${client.activeCases > 0 ? 'badge-green' : 'badge-slate'}`}
              >
                {client.activeCases} caso{client.activeCases !== 1 ? 's' : ''}
              </span>
            </div>

            <div className="mt-4 space-y-2">
              <div className="flex items-center gap-2 text-sm text-slate-600">
                <Mail className="h-3.5 w-3.5 shrink-0 text-slate-400" />
                <span className="truncate">{client.email}</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-slate-600">
                <Phone className="h-3.5 w-3.5 shrink-0 text-slate-400" />
                <span>{formatPhone(client.phone)}</span>
              </div>
              {client.cpf && (
                <p className="text-xs text-slate-400">CPF: {formatCPF(client.cpf)}</p>
              )}
            </div>

            <div className="mt-4 flex items-center justify-between border-t border-slate-100 pt-3">
              <p className="text-xs text-slate-400">Cliente desde {formatDate(client.createdAt)}</p>
              <button className="text-xs font-medium text-blue-600 hover:text-blue-700">
                Ver detalhes →
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Summary */}
      <p className="mt-4 text-sm text-slate-500">
        Total: <span className="font-medium">{clients.length} clientes</span>
      </p>
    </div>
  )
}
