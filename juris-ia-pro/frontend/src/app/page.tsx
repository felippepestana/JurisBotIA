'use client'

import Link from 'next/link'
import { Button } from '@/components/ui'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
      {/* Header */}
      <header className="container-custom py-6">
        <nav className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-secondary-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">⚖️</span>
            </div>
            <span className="text-2xl font-bold gradient-text">JurisIA Pro</span>
          </div>

          <div className="flex items-center gap-4">
            <Link href="/search">
              <Button variant="ghost">Buscar</Button>
            </Link>
            <Link href="/chat">
              <Button variant="ghost">Chat</Button>
            </Link>
            <Link href="/analyze">
              <Button variant="outline">Analisar PDF</Button>
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <main className="container-custom section-padding">
        <div className="text-center max-w-4xl mx-auto space-y-8">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-white rounded-full shadow-sm border border-primary-200">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            <span className="text-sm font-medium text-gray-700">Sistema operacional</span>
          </div>

          {/* Heading */}
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold leading-tight">
            Sistema Jurídico
            <br />
            <span className="gradient-text">Inteligente com IA</span>
          </h1>

          {/* Description */}
          <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
            Busca jurídica avançada, chat com IA especializada, análise automática de processos
            e geração de documentos legais. Tudo em uma plataforma.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <Link href="/search">
              <Button size="lg" className="min-w-[200px]">
                Começar Busca
              </Button>
            </Link>
            <Link href="/chat">
              <Button size="lg" variant="outline" className="min-w-[200px]">
                Chat com JUSIA
              </Button>
            </Link>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-6 pt-16">
            {/* Feature 1 */}
            <div className="bg-white p-6 rounded-2xl shadow-soft hover:shadow-lg transition-all duration-200 border border-gray-100">
              <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center mb-4">
                <span className="text-2xl">🔍</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">Busca Inteligente</h3>
              <p className="text-gray-600 text-sm">
                Busca semântica com IA em milhares de documentos jurídicos, leis e jurisprudência
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-white p-6 rounded-2xl shadow-soft hover:shadow-lg transition-all duration-200 border border-gray-100">
              <div className="w-12 h-12 bg-secondary-100 rounded-xl flex items-center justify-center mb-4">
                <span className="text-2xl">💬</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">Chat Jurídico</h3>
              <p className="text-gray-600 text-sm">
                Converse com JUSIA, assistente jurídica com IA, para tirar dúvidas e pesquisar
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-white p-6 rounded-2xl shadow-soft hover:shadow-lg transition-all duration-200 border border-gray-100">
              <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mb-4">
                <span className="text-2xl">📄</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">Análise de Processos</h3>
              <p className="text-gray-600 text-sm">
                Upload de PDF para análise automática com sugestão de framework legal aplicável
              </p>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-8 pt-16 max-w-3xl mx-auto">
            <div>
              <div className="text-4xl font-bold text-primary-600">100+</div>
              <div className="text-sm text-gray-600 mt-1">Documentos Indexados</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-secondary-600">50ms</div>
              <div className="text-sm text-gray-600 mt-1">Tempo de Resposta</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-green-600">98%</div>
              <div className="text-sm text-gray-600 mt-1">Confiança</div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="container-custom py-8 border-t border-gray-200 mt-20">
        <div className="text-center text-sm text-gray-600">
          <p>© 2025 JurisIA Pro. Desenvolvido com ⚖️ para revolucionar o acesso à justiça.</p>
        </div>
      </footer>
    </div>
  )
}
