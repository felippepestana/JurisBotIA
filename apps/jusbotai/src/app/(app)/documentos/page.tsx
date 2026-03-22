import { Plus, Search, Download, FileText } from 'lucide-react'
import { Header } from '@/components/layout/Header'
import { formatDate } from '@/lib/utils'

const documents = [
  {
    id: '1',
    title: 'Petição Inicial - Ação de Indenização',
    category: 'peticao',
    caseNumber: '0001234-56.2024.8.26.0100',
    client: 'Maria Silva Santos',
    createdAt: '2024-01-10',
    size: '245 KB',
  },
  {
    id: '2',
    title: 'Contrato de Prestação de Serviços Advocatícios',
    category: 'contrato',
    caseNumber: undefined,
    client: 'João Pedro Oliveira',
    createdAt: '2024-01-15',
    size: '128 KB',
  },
  {
    id: '3',
    title: 'Procuração Ad Judicia et Extra',
    category: 'procuracao',
    caseNumber: '0009876-54.2024.8.26.0200',
    client: 'João Pedro Oliveira',
    createdAt: '2024-01-15',
    size: '87 KB',
  },
  {
    id: '4',
    title: 'Recurso de Apelação',
    category: 'recurso',
    caseNumber: '0005432-10.2023.8.26.0050',
    client: 'Empresa ABC Ltda',
    createdAt: '2024-01-28',
    size: '512 KB',
  },
  {
    id: '5',
    title: 'Notificação Extrajudicial',
    category: 'notificacao',
    caseNumber: undefined,
    client: 'Carlos Eduardo Lima',
    createdAt: '2024-02-01',
    size: '156 KB',
  },
  {
    id: '6',
    title: 'Contestação - Execução Trabalhista',
    category: 'peticao',
    caseNumber: '0005432-10.2023.8.26.0050',
    client: 'Empresa ABC Ltda',
    createdAt: '2024-02-05',
    size: '324 KB',
  },
]

const categoryLabels: Record<string, string> = {
  peticao: 'Petição',
  contrato: 'Contrato',
  procuracao: 'Procuração',
  recurso: 'Recurso',
  notificacao: 'Notificação',
  outro: 'Outro',
}

const categoryColors: Record<string, string> = {
  peticao: 'badge-blue',
  contrato: 'badge-green',
  procuracao: 'badge-yellow',
  recurso: 'badge-red',
  notificacao: 'badge-slate',
  outro: 'badge-slate',
}

const categoryIcons: Record<string, string> = {
  peticao: '📄',
  contrato: '📋',
  procuracao: '✍️',
  recurso: '⚖️',
  notificacao: '📬',
  outro: '📁',
}

export default function DocumentosPage() {
  return (
    <div className="p-6">
      <Header title="Documentos" subtitle="Biblioteca de documentos e templates jurídicos" />

      {/* Actions bar */}
      <div className="mt-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex gap-2">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Buscar documentos..."
              className="w-64 rounded-lg border border-slate-200 bg-white py-2 pl-9 pr-4 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>
          <select className="form-select rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500">
            <option value="">Todas as categorias</option>
            {Object.entries(categoryLabels).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </div>
        <button className="btn-primary">
          <Plus className="h-4 w-4" />
          Novo Documento
        </button>
      </div>

      {/* Documents grid */}
      <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {documents.map((doc) => (
          <div
            key={doc.id}
            className="card cursor-pointer transition-shadow hover:shadow-md"
          >
            <div className="flex items-start gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-slate-100 text-xl">
                {categoryIcons[doc.category] ?? '📁'}
              </div>
              <div className="min-w-0 flex-1">
                <p className="truncate font-medium text-slate-900">{doc.title}</p>
                <span className={`mt-1 inline-flex ${categoryColors[doc.category] ?? 'badge-slate'}`}>
                  {categoryLabels[doc.category] ?? doc.category}
                </span>
              </div>
            </div>

            <div className="mt-4 space-y-1.5 text-sm text-slate-600">
              <p>
                <span className="text-slate-400">Cliente:</span> {doc.client}
              </p>
              {doc.caseNumber && (
                <p className="truncate font-mono text-xs text-slate-400">{doc.caseNumber}</p>
              )}
            </div>

            <div className="mt-4 flex items-center justify-between border-t border-slate-100 pt-3">
              <div>
                <p className="text-xs text-slate-400">{formatDate(doc.createdAt)}</p>
                <p className="text-xs text-slate-400">{doc.size}</p>
              </div>
              <div className="flex gap-2">
                <button
                  className="rounded p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-600"
                  aria-label="Visualizar documento"
                >
                  <FileText className="h-4 w-4" />
                </button>
                <button
                  className="rounded p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-600"
                  aria-label="Baixar documento"
                >
                  <Download className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Summary */}
      <p className="mt-4 text-sm text-slate-500">
        Total: <span className="font-medium">{documents.length} documentos</span>
      </p>
    </div>
  )
}
