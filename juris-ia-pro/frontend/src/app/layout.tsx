import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })

export const metadata: Metadata = {
  title: 'JurisIA Pro - Sistema Jurídico Inteligente',
  description: 'Busca jurídica avançada com IA, chat jurídico e análise de processos',
  keywords: ['jurisprudência', 'direito', 'IA', 'busca jurídica', 'análise legal'],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
