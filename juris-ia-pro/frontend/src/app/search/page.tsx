'use client'

import { useState, useCallback, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { FiSearch, FiFilter, FiX } from 'react-icons/fi'
import { Input, Button, Card, Badge, Loading } from '@/components/ui'
import { apiClient } from '@/lib/api'
import { debounce, formatDate, formatRelativeDate, TIPO_DOCUMENTO_LABELS, TIPO_DOCUMENTO_COLORS } from '@/lib/utils'
import type { SearchRequest, SearchResponse, SearchResult } from '@/types/api'

export default function SearchPage() {
  const router = useRouter()
  const searchParams = useSearchParams()

  const [query, setQuery] = useState(searchParams.get('q') || '')
  const [results, setResults] = useState<SearchResult[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [showFilters, setShowFilters] = useState(false)
  const [totalResults, setTotalResults] = useState(0)
  const [searchTime, setSearchTime] = useState(0)

  // Filtros
  const [filters, setFilters] = useState({
    tipo_documento: '',
    instancia: '',
    data_inicio: '',
    data_fim: '',
  })

  // Buscar sugestões de keywords
  const fetchSuggestions = useCallback(
    debounce(async (value: string) => {
      if (value.length < 2) {
        setSuggestions([])
        return
      }

      try {
        const data = await apiClient.getKeywordSuggestions(value)
        setSuggestions(data.suggestions)
      } catch (err) {
        console.error('Erro ao buscar sugestões:', err)
      }
    }, 300),
    []
  )

  // Realizar busca
  const handleSearch = async (searchQuery?: string) => {
    const q = searchQuery || query

    if (!q.trim()) {
      setError('Digite algo para buscar')
      return
    }

    setIsLoading(true)
    setError(null)
    setSuggestions([])

    try {
      const params: SearchRequest = {
        query: q,
        limit: 20,
        ...filters,
      }

      const data = await apiClient.search(params)

      setResults(data.results)
      setTotalResults(data.total)
      setSearchTime(data.time_ms)

      // Atualizar URL
      const params_url = new URLSearchParams({ q })
      router.push(`/search?${params_url.toString()}`)
    } catch (err: any) {
      setError(err.detail || 'Erro ao realizar busca')
      setResults([])
    } finally {
      setIsLoading(false)
    }
  }

  // Executar busca ao carregar se houver query na URL
  useEffect(() => {
    const q = searchParams.get('q')
    if (q) {
      setQuery(q)
      handleSearch(q)
    }
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
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
              <Button variant="ghost" onClick={() => router.push('/chat')}>
                Chat
              </Button>
              <Button variant="outline" onClick={() => router.push('/analyze')}>
                Analisar PDF
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container-custom py-8">
        {/* Search Bar */}
        <div className="max-w-4xl mx-auto mb-8">
          <div className="relative">
            <Input
              placeholder="Buscar jurisprudência, leis, súmulas..."
              value={query}
              onChange={(e) => {
                setQuery(e.target.value)
                fetchSuggestions(e.target.value)
              }}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleSearch()
                }
              }}
              leftIcon={<FiSearch className="w-5 h-5" />}
              rightIcon={
                query && (
                  <button
                    onClick={() => {
                      setQuery('')
                      setSuggestions([])
                      setResults([])
                    }}
                    className="hover:text-gray-700"
                  >
                    <FiX className="w-5 h-5" />
                  </button>
                )
              }
              className="text-lg py-3"
              autoFocus
            />

            {/* Sugestões */}
            {suggestions.length > 0 && (
              <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-lg shadow-lg z-20 max-h-80 overflow-y-auto">
                {suggestions.map((suggestion, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setQuery(suggestion)
                      setSuggestions([])
                      handleSearch(suggestion)
                    }}
                    className="w-full px-4 py-3 text-left hover:bg-gray-50 border-b last:border-b-0 transition-colors"
                  >
                    <div className="flex items-center gap-2">
                      <FiSearch className="w-4 h-4 text-gray-400" />
                      <span className="text-gray-700">{suggestion}</span>
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Actions */}
          <div className="flex items-center gap-3 mt-4">
            <Button
              onClick={() => handleSearch()}
              isLoading={isLoading}
              leftIcon={<FiSearch />}
            >
              Buscar
            </Button>

            <Button
              variant="outline"
              onClick={() => setShowFilters(!showFilters)}
              leftIcon={<FiFilter />}
            >
              Filtros
            </Button>

            {(filters.tipo_documento || filters.instancia) && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => {
                  setFilters({
                    tipo_documento: '',
                    instancia: '',
                    data_inicio: '',
                    data_fim: '',
                  })
                }}
              >
                Limpar filtros
              </Button>
            )}
          </div>

          {/* Filtros */}
          {showFilters && (
            <Card className="mt-4 animate-slide-down">
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tipo de Documento
                  </label>
                  <select
                    value={filters.tipo_documento}
                    onChange={(e) => setFilters({ ...filters, tipo_documento: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="">Todos</option>
                    <option value="lei">Lei</option>
                    <option value="sumula">Súmula</option>
                    <option value="acordao">Acórdão</option>
                    <option value="decreto">Decreto</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Instância
                  </label>
                  <select
                    value={filters.instancia}
                    onChange={(e) => setFilters({ ...filters, instancia: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="">Todas</option>
                    <option value="STF">STF</option>
                    <option value="STJ">STJ</option>
                    <option value="TST">TST</option>
                    <option value="TJSP">TJSP</option>
                    <option value="FEDERAL">Federal</option>
                  </select>
                </div>
              </div>
            </Card>
          )}
        </div>

        {/* Results Info */}
        {!isLoading && results.length > 0 && (
          <div className="max-w-4xl mx-auto mb-6 text-sm text-gray-600">
            <p>
              Encontrados <strong>{totalResults}</strong> resultados em{' '}
              <strong>{searchTime}ms</strong>
            </p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="max-w-4xl mx-auto mb-6">
            <Card className="bg-red-50 border-red-200">
              <p className="text-red-800">{error}</p>
            </Card>
          </div>
        )}

        {/* Loading */}
        {isLoading && (
          <div className="max-w-4xl mx-auto py-12">
            <Loading size="lg" text="Buscando documentos..." />
          </div>
        )}

        {/* Results */}
        {!isLoading && results.length > 0 && (
          <div className="max-w-4xl mx-auto space-y-4">
            {results.map((result) => (
              <Card
                key={result.id}
                hover
                className="cursor-pointer"
                onClick={() => router.push(`/document/${result.id}`)}
              >
                {/* Header */}
                <div className="flex items-start justify-between gap-4 mb-3">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-1 hover:text-primary-600 transition-colors">
                      {result.titulo}
                    </h3>
                    {result.orgao_emissor && (
                      <p className="text-sm text-gray-600">{result.orgao_emissor}</p>
                    )}
                  </div>

                  <Badge variant="info" className={TIPO_DOCUMENTO_COLORS[result.tipo_documento]}>
                    {TIPO_DOCUMENTO_LABELS[result.tipo_documento]}
                  </Badge>
                </div>

                {/* Ementa */}
                {result.ementa && (
                  <p className="text-gray-700 mb-3 leading-relaxed">
                    {result.ementa.length > 200
                      ? result.ementa.slice(0, 200) + '...'
                      : result.ementa}
                  </p>
                )}

                {/* Highlight */}
                {result.highlight && (
                  <div className="bg-yellow-50 border-l-4 border-yellow-400 p-3 mb-3 rounded">
                    <p
                      className="text-sm text-gray-700"
                      dangerouslySetInnerHTML={{ __html: result.highlight }}
                    />
                  </div>
                )}

                {/* Footer */}
                <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                  <div className="flex items-center gap-4 text-sm text-gray-500">
                    {result.data_publicacao && (
                      <span>📅 {formatDate(result.data_publicacao, 'dd/MM/yyyy')}</span>
                    )}
                    <span>⭐ {result.similarity_score?.toFixed(2) || result.relevancia_score.toFixed(2)}</span>
                    <span>📚 {result.citacoes_count} citações</span>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}

        {/* No Results */}
        {!isLoading && results.length === 0 && query && !error && (
          <div className="max-w-4xl mx-auto py-12 text-center">
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Nenhum resultado encontrado
            </h3>
            <p className="text-gray-600 mb-6">
              Tente usar termos diferentes ou remover filtros
            </p>
            <Button
              variant="outline"
              onClick={() => {
                setQuery('')
                setFilters({
                  tipo_documento: '',
                  instancia: '',
                  data_inicio: '',
                  data_fim: '',
                })
                setResults([])
              }}
            >
              Limpar busca
            </Button>
          </div>
        )}

        {/* Initial State */}
        {!isLoading && results.length === 0 && !query && !error && (
          <div className="max-w-4xl mx-auto py-12 text-center">
            <div className="text-6xl mb-4">⚖️</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Busca Jurídica Inteligente
            </h3>
            <p className="text-gray-600 mb-6">
              Digite sua consulta acima para buscar em nossa base de documentos jurídicos
            </p>

            <div className="grid md:grid-cols-3 gap-4 max-w-2xl mx-auto text-left">
              <button
                onClick={() => {
                  setQuery('CDC instituições financeiras')
                  handleSearch('CDC instituições financeiras')
                }}
                className="p-4 bg-white rounded-lg border border-gray-200 hover:border-primary-300 hover:shadow-md transition-all text-left"
              >
                <p className="text-sm font-medium text-gray-900 mb-1">Exemplo 1</p>
                <p className="text-xs text-gray-600">CDC instituições financeiras</p>
              </button>

              <button
                onClick={() => {
                  setQuery('dano moral')
                  handleSearch('dano moral')
                }}
                className="p-4 bg-white rounded-lg border border-gray-200 hover:border-primary-300 hover:shadow-md transition-all text-left"
              >
                <p className="text-sm font-medium text-gray-900 mb-1">Exemplo 2</p>
                <p className="text-xs text-gray-600">dano moral</p>
              </button>

              <button
                onClick={() => {
                  setQuery('superendividamento')
                  handleSearch('superendividamento')
                }}
                className="p-4 bg-white rounded-lg border border-gray-200 hover:border-primary-300 hover:shadow-md transition-all text-left"
              >
                <p className="text-sm font-medium text-gray-900 mb-1">Exemplo 3</p>
                <p className="text-xs text-gray-600">superendividamento</p>
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
