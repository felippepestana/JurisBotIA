// Case status options
export type CaseStatus = 'ativo' | 'encerrado' | 'suspenso' | 'aguardando'

// Case priority levels
export type CasePriority = 'alta' | 'media' | 'baixa'

// Document template categories
export type DocumentCategory =
  | 'peticao'
  | 'contrato'
  | 'procuracao'
  | 'recurso'
  | 'notificacao'
  | 'outro'

// Client type
export interface Client {
  id: string
  name: string
  email: string
  phone: string
  cpf?: string
  cnpj?: string
  address?: string
  city?: string
  state?: string
  createdAt: string
  updatedAt: string
}

// Legal case / process
export interface Case {
  id: string
  number: string
  title: string
  description?: string
  status: CaseStatus
  priority: CasePriority
  clientId: string
  client?: Client
  court?: string
  judge?: string
  openedAt: string
  closedAt?: string
  nextHearing?: string
  createdAt: string
  updatedAt: string
}

// Legal document
export interface Document {
  id: string
  title: string
  category: DocumentCategory
  caseId?: string
  case?: Case
  clientId?: string
  client?: Client
  content?: string
  fileUrl?: string
  createdAt: string
  updatedAt: string
}

// Deadline / event
export interface Deadline {
  id: string
  title: string
  description?: string
  dueDate: string
  completed: boolean
  caseId?: string
  case?: Case
  clientId?: string
  client?: Client
  createdAt: string
  updatedAt: string
}

// Dashboard statistics
export interface DashboardStats {
  activeCases: number
  totalClients: number
  pendingDeadlines: number
  documentsGenerated: number
}

// Navigation item
export interface NavItem {
  label: string
  href: string
  icon: string
}
