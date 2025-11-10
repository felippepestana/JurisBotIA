'use client'

import { useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { FiUpload, FiFile, FiX, FiCheckCircle } from 'react-icons/fi'
import { Button, Card, CardHeader, CardTitle, CardContent, Badge, Loading } from '@/components/ui'
import { apiClient } from '@/lib/api'
import { formatFileSize, TIPO_DOCUMENTO_LABELS } from '@/lib/utils'
import type { PDFAnalysisResponse, LegalFrameworkItem } from '@/types/api'

export default function AnalyzePage() {
  const router = useRouter()
  const [file, setFile] = useState<File | null>(null)
  const [isDragging, setIsDragging] = useState(false)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysis, setAnalysis] = useState<PDFAnalysisResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [analysisType, setAnalysisType] = useState<'completa' | 'rapida' | 'riscos'>('completa')

  // Handle drag and drop
  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }, [])

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)

    const files = e.dataTransfer.files
    if (files && files[0]) {
      handleFileSelect(files[0])
    }
  }, [])

  // Handle file selection
  const handleFileSelect = (selectedFile: File) => {
    // Validar tipo de arquivo
    if (selectedFile.type !== 'application/pdf') {
      setError('Por favor, selecione um arquivo PDF')
      return
    }

    // Validar tamanho (max 20MB)
    if (selectedFile.size > 20 * 1024 * 1024) {
      setError('Arquivo muito grande. Tamanho máximo: 20MB')
      return
    }

    setFile(selectedFile)
    setError(null)
    setAnalysis(null)
  }

  // Analisar PDF
  const handleAnalyze = async () => {
    if (!file) return

    setIsAnalyzing(true)
    setError(null)

    try {
      const response = await apiClient.analyzePDF(file, analysisType)
      setAnalysis(response)
    } catch (err: any) {
      setError(err.detail || 'Erro ao analisar PDF')
    } finally {
      setIsAnalyzing(false)
    }
  }

  // Reset
  const handleReset = () => {
    setFile(null)
    setAnalysis(null)
    setError(null)
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
        <div className="max-w-5xl mx-auto">
          {/* Title */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-3">
              Análise de Processos Judiciais
            </h1>
            <p className="text-lg text-gray-600">
              Faça upload de um PDF para análise automática com IA
            </p>
          </div>

          {/* Upload Section */}
          {!analysis && (
            <Card className="mb-6">
              {/* File input area */}
              <div
                onDragEnter={handleDragEnter}
                onDragLeave={handleDragLeave}
                onDragOver={handleDragOver}
                onDrop={handleDrop}
                className={`border-2 border-dashed rounded-xl p-12 text-center transition-all ${
                  isDragging
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-300 hover:border-primary-400'
                }`}
              >
                {!file ? (
                  <>
                    <FiUpload className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                    <p className="text-lg font-medium text-gray-900 mb-2">
                      Arraste seu PDF aqui ou clique para selecionar
                    </p>
                    <p className="text-sm text-gray-600 mb-6">
                      Tamanho máximo: 20MB • Formato: PDF
                    </p>
                    <label>
                      <input
                        type="file"
                        accept=".pdf,application/pdf"
                        onChange={(e) => {
                          const file = e.target.files?.[0]
                          if (file) handleFileSelect(file)
                        }}
                        className="hidden"
                      />
                      <Button as="span" className="cursor-pointer">
                        Selecionar Arquivo
                      </Button>
                    </label>
                  </>
                ) : (
                  <div className="flex items-center justify-between bg-gray-50 p-4 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
                        <FiFile className="w-6 h-6 text-red-600" />
                      </div>
                      <div className="text-left">
                        <p className="font-medium text-gray-900">{file.name}</p>
                        <p className="text-sm text-gray-600">{formatFileSize(file.size)}</p>
                      </div>
                    </div>
                    <button
                      onClick={handleReset}
                      className="p-2 hover:bg-gray-200 rounded-lg transition-colors"
                    >
                      <FiX className="w-5 h-5 text-gray-600" />
                    </button>
                  </div>
                )}
              </div>

              {/* Analysis type */}
              {file && (
                <div className="mt-6">
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Tipo de Análise
                  </label>
                  <div className="grid md:grid-cols-3 gap-3">
                    <button
                      onClick={() => setAnalysisType('rapida')}
                      className={`p-4 rounded-lg border-2 text-left transition-all ${
                        analysisType === 'rapida'
                          ? 'border-primary-500 bg-primary-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <p className="font-medium text-gray-900 mb-1">Análise Rápida</p>
                      <p className="text-xs text-gray-600">
                        Identificação básica do tipo e partes
                      </p>
                    </button>

                    <button
                      onClick={() => setAnalysisType('completa')}
                      className={`p-4 rounded-lg border-2 text-left transition-all ${
                        analysisType === 'completa'
                          ? 'border-primary-500 bg-primary-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <p className="font-medium text-gray-900 mb-1">Análise Completa</p>
                      <p className="text-xs text-gray-600">
                        Framework legal e recomendações
                      </p>
                    </button>

                    <button
                      onClick={() => setAnalysisType('riscos')}
                      className={`p-4 rounded-lg border-2 text-left transition-all ${
                        analysisType === 'riscos'
                          ? 'border-primary-500 bg-primary-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <p className="font-medium text-gray-900 mb-1">Análise de Riscos</p>
                      <p className="text-xs text-gray-600">
                        Identificação de vulnerabilidades
                      </p>
                    </button>
                  </div>
                </div>
              )}

              {/* Error */}
              {error && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-red-800">{error}</p>
                </div>
              )}

              {/* Analyze button */}
              {file && !isAnalyzing && (
                <div className="mt-6">
                  <Button
                    onClick={handleAnalyze}
                    size="lg"
                    fullWidth
                    leftIcon={<FiCheckCircle />}
                  >
                    Analisar Documento
                  </Button>
                </div>
              )}

              {/* Loading */}
              {isAnalyzing && (
                <div className="mt-6 py-8">
                  <Loading
                    size="lg"
                    text="Analisando documento com IA... Isso pode levar alguns segundos"
                  />
                </div>
              )}
            </Card>
          )}

          {/* Results */}
          {analysis && (
            <div className="space-y-6 animate-fade-in">
              {/* Header */}
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-gray-900">Resultado da Análise</h2>
                <Button variant="outline" onClick={handleReset}>
                  Nova Análise
                </Button>
              </div>

              {/* Info básica */}
              <Card>
                <CardHeader>
                  <CardTitle>Informações do Documento</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-600 mb-1">Arquivo</p>
                      <p className="font-medium">{analysis.filename}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 mb-1">Páginas</p>
                      <p className="font-medium">{analysis.metadata.pages}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 mb-1">Tipo de Documento</p>
                      <Badge variant="info">{analysis.analysis.document_type}</Badge>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 mb-1">Área do Direito</p>
                      <Badge variant="primary">{analysis.analysis.legal_area}</Badge>
                    </div>
                  </div>

                  {/* Confiança */}
                  <div className="mt-4">
                    <div className="flex items-center justify-between text-sm mb-2">
                      <span className="text-gray-600">Confiança da Análise</span>
                      <span className="font-medium">{(analysis.analysis.confidence_score * 100).toFixed(0)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-primary-600 h-2 rounded-full transition-all"
                        style={{ width: `${analysis.analysis.confidence_score * 100}%` }}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Partes */}
              {analysis.analysis.parties.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle>Partes Identificadas</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex flex-wrap gap-2">
                      {analysis.analysis.parties.map((party, idx) => (
                        <Badge key={idx} variant="secondary">
                          {party}
                        </Badge>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Questões principais */}
              {analysis.analysis.key_issues.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle>Questões Jurídicas Principais</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {analysis.analysis.key_issues.map((issue, idx) => (
                        <li key={idx} className="flex items-start gap-2">
                          <span className="text-primary-600 mt-1">•</span>
                          <span className="text-gray-700">{issue}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}

              {/* Framework Legal */}
              {analysis.analysis.applicable_framework.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle>Framework Legal Aplicável</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {analysis.analysis.applicable_framework.map((item, idx) => (
                        <div
                          key={idx}
                          className="p-4 bg-gray-50 rounded-lg border border-gray-200"
                        >
                          <div className="flex items-start justify-between mb-2">
                            <p className="font-medium text-gray-900">{item.documento}</p>
                            <Badge
                              variant={
                                item.aplicabilidade === 'Alta'
                                  ? 'success'
                                  : item.aplicabilidade === 'Média'
                                  ? 'warning'
                                  : 'default'
                              }
                            >
                              {item.aplicabilidade}
                            </Badge>
                          </div>
                          <p className="text-sm text-gray-700">{item.fundamento}</p>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Recomendações */}
              {analysis.analysis.recommendations.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle>Recomendações</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-3">
                      {analysis.analysis.recommendations.map((rec, idx) => (
                        <li
                          key={idx}
                          className="flex items-start gap-3 p-3 bg-primary-50 rounded-lg"
                        >
                          <FiCheckCircle className="w-5 h-5 text-primary-600 flex-shrink-0 mt-0.5" />
                          <span className="text-gray-800">{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}

              {/* Tempo de processamento */}
              <div className="text-center text-sm text-gray-600">
                <p>Análise concluída em {(analysis.time_ms / 1000).toFixed(1)}s</p>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
