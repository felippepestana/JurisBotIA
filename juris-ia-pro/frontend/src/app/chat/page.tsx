'use client'

import { useState, useRef, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { FiSend, FiUser } from 'react-icons/fi'
import ReactMarkdown from 'react-markdown'
import { Button, Card, Badge, Loading, TextArea } from '@/components/ui'
import { apiClient } from '@/lib/api'
import { formatRelativeDate, getConfidenceColor, getConfidenceLabel } from '@/lib/utils'
import type { ChatResponse, SourceReference } from '@/types/api'

interface Message {
  role: 'user' | 'assistant'
  content: string
  sources?: SourceReference[]
  confidence?: number
  timestamp: Date
  processing_time?: number
}

export default function ChatPage() {
  const router = useRouter()
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [conversationId, setConversationId] = useState<string>()
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Auto-scroll para última mensagem
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Enviar mensagem
  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await apiClient.chat({
        message: input,
        conversation_id: conversationId,
      })

      setConversationId(response.conversation_id)

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response,
        sources: response.sources,
        confidence: response.confidence,
        timestamp: new Date(),
        processing_time: response.processing_time_ms,
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (err: any) {
      const errorMessage: Message = {
        role: 'assistant',
        content: `Erro: ${err.detail || 'Não foi possível processar sua mensagem'}`,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
      textareaRef.current?.focus()
    }
  }

  // Perguntas sugeridas
  const suggestedQuestions = [
    'O CDC se aplica a instituições financeiras?',
    'Quais são os casos de dano moral reconhecidos?',
    'O que é superendividamento?',
    'Explique a inversão do ônus da prova',
  ]

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
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
              <div className="hidden sm:block">
                <Badge variant="info">JUSIA - Assistente Jurídica</Badge>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <Button variant="ghost" onClick={() => router.push('/search')}>
                Buscar
              </Button>
              <Button variant="outline" onClick={() => router.push('/analyze')}>
                Analisar PDF
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Chat Container */}
      <div className="flex-1 container-custom py-6 flex flex-col max-w-5xl">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto custom-scrollbar mb-6 space-y-6">
          {/* Mensagem de boas-vindas */}
          {messages.length === 0 && (
            <div className="text-center py-12">
              <div className="w-20 h-20 bg-gradient-to-br from-primary-600 to-secondary-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-4xl">🤖</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                Olá! Sou a JUSIA
              </h2>
              <p className="text-gray-600 mb-8 max-w-md mx-auto">
                Sua assistente jurídica com inteligência artificial. Pergunte sobre legislação,
                jurisprudência ou tire dúvidas jurídicas.
              </p>

              {/* Perguntas sugeridas */}
              <div className="max-w-2xl mx-auto">
                <p className="text-sm font-medium text-gray-700 mb-3">Perguntas sugeridas:</p>
                <div className="grid md:grid-cols-2 gap-3">
                  {suggestedQuestions.map((question, idx) => (
                    <button
                      key={idx}
                      onClick={() => {
                        setInput(question)
                        textareaRef.current?.focus()
                      }}
                      className="p-4 text-left bg-white rounded-lg border border-gray-200 hover:border-primary-300 hover:shadow-md transition-all"
                    >
                      <p className="text-sm text-gray-700">{question}</p>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Mensagens da conversa */}
          {messages.map((message, idx) => (
            <div
              key={idx}
              className={`flex gap-4 ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {message.role === 'assistant' && (
                <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-secondary-600 rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-white text-xl">🤖</span>
                </div>
              )}

              <div
                className={`max-w-3xl ${
                  message.role === 'user' ? 'order-first' : ''
                }`}
              >
                <Card
                  padding="md"
                  className={`${
                    message.role === 'user'
                      ? 'bg-primary-600 text-white'
                      : 'bg-white'
                  }`}
                >
                  <div
                    className={`legal-content prose ${
                      message.role === 'user'
                        ? 'prose-invert'
                        : 'prose-gray'
                    }`}
                  >
                    <ReactMarkdown>{message.content}</ReactMarkdown>
                  </div>

                  {/* Fontes */}
                  {message.sources && message.sources.length > 0 && (
                    <div className="mt-4 pt-4 border-t border-gray-200">
                      <p className="text-sm font-medium text-gray-700 mb-2">
                        📚 Fontes consultadas:
                      </p>
                      <div className="space-y-2">
                        {message.sources.map((source, sidx) => (
                          <div
                            key={sidx}
                            className="text-sm bg-gray-50 p-3 rounded border border-gray-200"
                          >
                            <p className="font-medium text-gray-900">{source.titulo}</p>
                            {source.orgao && (
                              <p className="text-xs text-gray-600 mt-1">{source.orgao}</p>
                            )}
                            {source.trecho_relevante && (
                              <p className="text-xs text-gray-700 mt-2 italic">
                                "{source.trecho_relevante}"
                              </p>
                            )}
                            <div className="flex items-center gap-2 mt-2">
                              <Badge size="sm" variant="info">
                                Confiança: {(source.confianca * 100).toFixed(0)}%
                              </Badge>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Metadata */}
                  <div
                    className={`flex items-center gap-3 text-xs mt-3 ${
                      message.role === 'user' ? 'text-primary-100' : 'text-gray-500'
                    }`}
                  >
                    <span>{formatRelativeDate(message.timestamp)}</span>
                    {message.confidence !== undefined && (
                      <>
                        <span>•</span>
                        <span className={getConfidenceColor(message.confidence)}>
                          {getConfidenceLabel(message.confidence)} confiança
                        </span>
                      </>
                    )}
                    {message.processing_time !== undefined && (
                      <>
                        <span>•</span>
                        <span>{message.processing_time}ms</span>
                      </>
                    )}
                  </div>
                </Card>
              </div>

              {message.role === 'user' && (
                <div className="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center flex-shrink-0">
                  <FiUser className="w-5 h-5 text-gray-700" />
                </div>
              )}
            </div>
          ))}

          {/* Loading indicator */}
          {isLoading && (
            <div className="flex gap-4">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-secondary-600 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-white text-xl">🤖</span>
              </div>
              <Card padding="md" className="bg-white">
                <Loading variant="dots" size="sm" />
              </Card>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="bg-white border border-gray-200 rounded-xl shadow-lg p-4">
          <div className="flex gap-3">
            <TextArea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault()
                  handleSend()
                }
              }}
              placeholder="Digite sua pergunta jurídica... (Shift+Enter para nova linha)"
              rows={3}
              className="flex-1 resize-none"
              disabled={isLoading}
            />
            <Button
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              isLoading={isLoading}
              className="self-end"
              leftIcon={<FiSend />}
            >
              Enviar
            </Button>
          </div>

          <div className="flex items-center justify-between mt-3 text-xs text-gray-500">
            <p>Pressione Enter para enviar, Shift+Enter para nova linha</p>
            {conversationId && (
              <p className="font-mono">ID: {conversationId.slice(0, 8)}...</p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
