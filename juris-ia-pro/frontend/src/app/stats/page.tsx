'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { FiRefreshCw, FiCpu, FiDatabase, FiZap } from 'react-icons/fi'
import { Button, Card, CardHeader, CardTitle, CardContent, Badge, Loading } from '@/components/ui'
import { apiClient } from '@/lib/api'
import { formatDate, formatNumber, formatDuration } from '@/lib/utils'
import type { SystemStats, PerformanceMetrics } from '@/types/api'

export default function StatsPage() {
  const router = useRouter()
  const [stats, setStats] = useState<SystemStats | null>(null)
  const [performance, setPerformance] = useState<PerformanceMetrics | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Carregar estatísticas
  const loadStats = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const [statsData, perfData] = await Promise.all([
        apiClient.getSystemStats(),
        apiClient.getPerformanceMetrics(),
      ])

      setStats(statsData)
      setPerformance(perfData)
    } catch (err: any) {
      setError(err.detail || 'Erro ao carregar estatísticas')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadStats()
  }, [])

  // Status color helper
  const getStatusColor = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'online':
      case 'available':
      case 'healthy':
        return 'success'
      case 'offline':
      case 'unavailable':
      case 'degraded':
        return 'danger'
      default:
        return 'warning'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="container-custom py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => router.push('/')}
                className="flex items-center gap-2 hover:opacity-80 transition-opacity"
              >
                <div className="w-8 h-8 bg-gradient-to-br from-primary-600 to-secondary-600 rounded-lg flex items-center justify-center">
                  <span className="text-white text-lg">⚖️</span>
                </div>
                <span className="text-xl font-bold gradient-text">JurisIA Pro</span>
              </button>
            </div>

            <div className="flex items-center gap-3">
              <Button
                variant="outline"
                leftIcon={<FiRefreshCw />}
                onClick={loadStats}
                disabled={isLoading}
              >
                Atualizar
              </Button>
              <Button variant="ghost" onClick={() => router.push('/search')}>
                Buscar
              </Button>
              <Button variant="ghost" onClick={() => router.push('/chat')}>
                Chat
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container-custom py-8">
        {/* Title */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Estatísticas do Sistema
          </h1>
          <p className="text-gray-600">
            Monitoramento em tempo real dos serviços e performance
          </p>
        </div>

        {/* Loading */}
        {isLoading && (
          <div className="py-12">
            <Loading size="lg" text="Carregando estatísticas..." />
          </div>
        )}

        {/* Error */}
        {error && !isLoading && (
          <Card className="bg-red-50 border-red-200">
            <p className="text-red-800">{error}</p>
          </Card>
        )}

        {/* Stats */}
        {stats && !isLoading && (
          <div className="space-y-6 animate-fade-in">
            {/* Status do Sistema */}
            <div className="grid md:grid-cols-3 gap-6">
              {/* Sistema */}
              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between mb-4">
                    <FiCpu className="w-8 h-8 text-primary-600" />
                    <Badge variant={getStatusColor(stats.system.status)}>
                      {stats.system.status}
                    </Badge>
                  </div>
                  <h3 className="text-lg font-semibold mb-1">Sistema</h3>
                  <p className="text-2xl font-bold text-gray-900">v{stats.system.version}</p>
                  <p className="text-sm text-gray-600 mt-1">
                    Uptime: {stats.system.uptime_check_ms}ms
                  </p>
                </CardContent>
              </Card>

              {/* Cache */}
              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between mb-4">
                    <FiZap className="w-8 h-8 text-yellow-600" />
                    <Badge variant={stats.services.redis.available ? 'success' : 'danger'}>
                      {stats.services.redis.status}
                    </Badge>
                  </div>
                  <h3 className="text-lg font-semibold mb-1">Redis Cache</h3>
                  {stats.cache && (
                    <>
                      <p className="text-2xl font-bold text-gray-900">
                        {formatNumber(stats.cache.total_keys)}
                      </p>
                      <p className="text-sm text-gray-600 mt-1">
                        chaves • {stats.cache.used_memory_human}
                      </p>
                    </>
                  )}
                </CardContent>
              </Card>

              {/* Vector DB */}
              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between mb-4">
                    <FiDatabase className="w-8 h-8 text-purple-600" />
                    <Badge variant={stats.services.qdrant.available ? 'success' : 'danger'}>
                      {stats.services.qdrant.status}
                    </Badge>
                  </div>
                  <h3 className="text-lg font-semibold mb-1">Qdrant</h3>
                  {stats.vector_database && (
                    <>
                      <p className="text-2xl font-bold text-gray-900">
                        {formatNumber(stats.vector_database.documents_indexed)}
                      </p>
                      <p className="text-sm text-gray-600 mt-1">
                        documentos indexados
                      </p>
                    </>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Serviços */}
            <Card>
              <CardHeader>
                <CardTitle>Status dos Serviços</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {/* Redis */}
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className={`w-3 h-3 rounded-full ${
                        stats.services.redis.available ? 'bg-green-500' : 'bg-red-500'
                      }`} />
                      <span className="font-medium">Redis Cache</span>
                    </div>
                    <Badge variant={stats.services.redis.available ? 'success' : 'danger'}>
                      {stats.services.redis.status}
                    </Badge>
                  </div>

                  {/* Qdrant */}
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className={`w-3 h-3 rounded-full ${
                        stats.services.qdrant.available ? 'bg-green-500' : 'bg-red-500'
                      }`} />
                      <span className="font-medium">Qdrant Vector Database</span>
                    </div>
                    <Badge variant={stats.services.qdrant.available ? 'success' : 'danger'}>
                      {stats.services.qdrant.status}
                    </Badge>
                  </div>

                  {/* OpenAI */}
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className={`w-3 h-3 rounded-full ${
                        stats.services.openai.available ? 'bg-green-500' : 'bg-red-500'
                      }`} />
                      <span className="font-medium">OpenAI API</span>
                    </div>
                    <Badge variant={stats.services.openai.available ? 'success' : 'danger'}>
                      {stats.services.openai.status}
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Performance Metrics */}
            {performance && (
              <Card>
                <CardHeader>
                  <CardTitle>Métricas de Performance</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-2 gap-6">
                    {/* Current Metrics */}
                    <div>
                      <h4 className="text-sm font-medium text-gray-700 mb-3">Métricas Atuais</h4>
                      <div className="space-y-3">
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600">Cache Roundtrip</span>
                          <span className="font-mono font-medium">
                            {performance.current_metrics.cache_roundtrip_ms !== null
                              ? `${performance.current_metrics.cache_roundtrip_ms.toFixed(2)}ms`
                              : 'N/A'}
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600">Vector Search</span>
                          <span className="font-mono font-medium">
                            {performance.current_metrics.vector_search_ms !== null
                              ? `${performance.current_metrics.vector_search_ms.toFixed(2)}ms`
                              : 'N/A'}
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Target Benchmarks */}
                    <div>
                      <h4 className="text-sm font-medium text-gray-700 mb-3">Benchmarks Esperados</h4>
                      <div className="space-y-3">
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600">Cache Hit</span>
                          <span className="font-mono text-green-600">
                            &lt; {performance.target_benchmarks.cache_hit_target_ms}ms
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600">Cache Miss</span>
                          <span className="font-mono text-yellow-600">
                            &lt; {performance.target_benchmarks.cache_miss_target_ms}ms
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600">Chat Response</span>
                          <span className="font-mono text-blue-600">
                            &lt; {performance.target_benchmarks.chat_response_target_ms}ms
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600">PDF Analysis</span>
                          <span className="font-mono text-purple-600">
                            &lt; {performance.target_benchmarks.pdf_analysis_target_ms}ms
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Configuração */}
            <Card>
              <CardHeader>
                <CardTitle>Configuração</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Ambiente</p>
                    <p className="font-medium capitalize">{stats.configuration.environment}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Cache TTL</p>
                    <p className="font-medium">{stats.configuration.cache_ttl_seconds}s</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">RAG Similarity Threshold</p>
                    <p className="font-medium">{stats.configuration.rag_similarity_threshold}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Timestamp</p>
                    <p className="font-medium text-sm">{formatDate(stats.timestamp, 'PPpp')}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </main>
    </div>
  )
}
