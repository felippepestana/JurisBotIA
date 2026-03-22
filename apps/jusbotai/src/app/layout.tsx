import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: {
    default: 'JusBotAi - Ferramenta de Assistência a Advocacia',
    template: '%s | JusBotAi',
  },
  description: 'Plataforma inteligente de assistência a advocacia com IA',
  keywords: ['advocacia', 'jurídico', 'IA', 'gestão de casos', 'processos'],
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="pt-BR">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
