# 🏛️ JurisIA Pro - Frontend

Frontend moderno e excepcional do JurisIA Pro, construído com Next.js 14, React 18 e TypeScript.

## 🎨 Features

- ✅ **Busca Jurídica Inteligente** - Interface de busca com autocompletar, filtros avançados e highlight
- ✅ **Chat com JUSIA** - Chat em tempo real com assistente jurídica alimentada por IA
- ✅ **Análise de PDF** - Upload e análise automática de processos judiciais
- ✅ **Dashboard de Estatísticas** - Monitoramento em tempo real do sistema
- ✅ **Design Responsivo** - 100% mobile-first e adaptável
- ✅ **Performance Otimizada** - Server-side rendering e caching inteligente

## 🚀 Stack Tecnológica

### Core
- **Next.js 14** - Framework React com App Router
- **React 18** - Biblioteca de UI
- **TypeScript 5** - Type safety
- **TailwindCSS 3** - Utility-first CSS

### Bibliotecas
- **Axios** - Cliente HTTP
- **Zustand** - State management (pronto para uso)
- **Date-fns** - Manipulação de datas em português
- **Framer Motion** - Animações suaves
- **React Markdown** - Renderização de markdown
- **React Icons** - Ícones SVG

## 📁 Estrutura do Projeto

```
frontend/
├── src/
│   ├── app/                    # Pages (App Router)
│   │   ├── page.tsx           # Homepage
│   │   ├── search/            # Busca jurídica
│   │   ├── chat/              # Chat com JUSIA
│   │   ├── analyze/           # Análise de PDF
│   │   ├── stats/             # Dashboard
│   │   ├── layout.tsx         # Layout raiz
│   │   └── globals.css        # Estilos globais
│   ├── components/
│   │   └── ui/                # Componentes reutilizáveis
│   │       ├── Button.tsx
│   │       ├── Card.tsx
│   │       ├── Input.tsx
│   │       ├── Badge.tsx
│   │       ├── Loading.tsx
│   │       └── index.ts
│   ├── lib/
│   │   ├── api.ts             # Cliente API
│   │   └── utils.ts           # Utilitários
│   └── types/
│       └── api.ts             # Tipos TypeScript
├── public/                     # Assets estáticos
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.js
```

## 🛠️ Setup e Instalação

### Pré-requisitos

- Node.js 18+
- npm ou yarn
- Backend do JurisIA Pro rodando (porta 8000)

### Instalação

```bash
# Instalar dependências
npm install

# Copiar arquivo de ambiente
cp .env.example .env

# Configurar variáveis de ambiente
nano .env
```

### Variáveis de Ambiente

```env
# API Backend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_PREFIX=/api/v1

# App Info
NEXT_PUBLIC_APP_NAME=JurisIA Pro
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### Executar em Desenvolvimento

```bash
npm run dev
```

Acesse: http://localhost:3000

### Build para Produção

```bash
# Criar build otimizado
npm run build

# Iniciar servidor de produção
npm start
```

## 📄 Páginas

### 1. Homepage (`/`)
- Hero section com gradiente
- 3 features principais
- Estatísticas do sistema
- CTAs para funcionalidades
- Design moderno e animado

### 2. Busca Jurídica (`/search`)
- Barra de busca com autocompletar
- Sugestões de keywords em tempo real
- Filtros avançados (tipo, instância, data)
- Resultados com highlight
- Cards hover com animação
- Performance otimizada com debounce

**Funcionalidades:**
- Busca por query string (`?q=termo`)
- Filtros persistentes
- Highlight de termos buscados
- Badges de tipo de documento
- Scores de relevância
- Metadata completa (data, órgão, citações)

### 3. Chat com JUSIA (`/chat`)
- Interface de chat moderna
- Mensagens em tempo real
- Markdown support para respostas
- Citação de fontes
- Badges de confiança
- Auto-scroll para última mensagem
- Perguntas sugeridas
- Conversation ID tracking

**Funcionalidades:**
- Enter para enviar, Shift+Enter para nova linha
- Loading state durante processamento
- Display de tempo de resposta
- Fontes expandíveis com trechos relevantes
- Histórico de conversa

### 4. Análise de PDF (`/analyze`)
- Drag and drop de arquivos
- Upload de PDF (max 20MB)
- 3 tipos de análise (rápida, completa, riscos)
- Progress indicator
- Resultados estruturados
- Framework legal sugerido

**Funcionalidades:**
- Validação de arquivo (tipo e tamanho)
- Preview de informações do PDF
- Identificação de partes
- Questões jurídicas principais
- Framework legal aplicável com scores
- Recomendações práticas
- Confiança da análise (%)

### 5. Dashboard de Estatísticas (`/stats`)
- Status dos serviços em tempo real
- Métricas de performance
- Estatísticas de cache
- Vector database info
- Configuração do sistema
- Auto-refresh

**Funcionalidades:**
- Status visual (verde/vermelho)
- Badges de status
- Métricas atuais vs benchmarks
- Timestamp de atualização
- Botão de refresh manual

## 🎨 Componentes UI

### Button
```tsx
<Button
  variant="primary|secondary|outline|ghost|danger"
  size="sm|md|lg"
  isLoading={false}
  leftIcon={<Icon />}
  rightIcon={<Icon />}
  fullWidth={false}
>
  Texto
</Button>
```

### Card
```tsx
<Card hover padding="sm|md|lg">
  <CardHeader>
    <CardTitle>Título</CardTitle>
    <CardDescription>Descrição</CardDescription>
  </CardHeader>
  <CardContent>
    Conteúdo
  </CardContent>
  <CardFooter>
    Footer
  </CardFooter>
</Card>
```

### Input & TextArea
```tsx
<Input
  label="Label"
  error="Mensagem de erro"
  helperText="Texto de ajuda"
  leftIcon={<Icon />}
  rightIcon={<Icon />}
  fullWidth
/>

<TextArea
  label="Label"
  rows={4}
  error="Mensagem de erro"
/>
```

### Badge
```tsx
<Badge
  variant="default|primary|secondary|success|warning|danger|info"
  size="sm|md|lg"
>
  Texto
</Badge>
```

### Loading
```tsx
<Loading
  size="sm|md|lg|xl"
  variant="spinner|dots|pulse"
  text="Carregando..."
  fullScreen={false}
/>
```

## 🎨 Design System

### Cores

#### Primary (Azul)
- 50 → 950: Escala completa de azul
- Uso: CTAs, links, elementos principais

#### Secondary (Roxo)
- 50 → 950: Escala completa de roxo
- Uso: Elementos secundários, badges

#### Legal (Jurídico)
- Gold: `#d4af37`
- Dark Blue: `#1e3a5f`
- Light Gray: `#f8f9fa`

### Tipografia

- **Sans**: Inter (padrão)
- **Serif**: Playfair Display (títulos)
- **Mono**: Fira Code (código)

### Tamanhos

- xs: 0.75rem
- sm: 0.875rem
- base: 1rem
- lg: 1.125rem
- xl: 1.25rem
- 2xl → 5xl: Escalando

### Animações

- `fade-in`: Fade suave
- `slide-up`: Slide de baixo para cima
- `slide-down`: Slide de cima para baixo
- `pulse-slow`: Pulse lento

## 🔧 Utilitários

### Formatação
```ts
import { formatDate, formatRelativeDate, formatFileSize, formatNumber } from '@/lib/utils'

formatDate(date, 'PPP') // 15 de janeiro de 2025
formatRelativeDate(date) // há 2 dias
formatFileSize(1024) // 1 KB
formatNumber(1000) // 1.000
```

### Helpers
```ts
import { cn, truncate, debounce, highlightText } from '@/lib/utils'

cn('class1', condition && 'class2') // Combina classes
truncate(text, 100) // Trunca com ellipsis
debounce(fn, 300) // Debounce function
highlightText(text, query) // Adiciona <mark>
```

## 📡 API Client

```ts
import { apiClient } from '@/lib/api'

// Busca
const results = await apiClient.search({ query: 'CDC', limit: 10 })

// Chat
const response = await apiClient.chat({ message: 'Pergunta', conversation_id: 'id' })

// Análise de PDF
const analysis = await apiClient.analyzePDF(file, 'completa')

// Estatísticas
const stats = await apiClient.getSystemStats()
```

## 🔒 Type Safety

Todos os tipos estão definidos em `src/types/api.ts`:

```ts
import type {
  SearchRequest,
  SearchResponse,
  ChatMessage,
  ChatResponse,
  PDFAnalysisResponse,
  SystemStats,
  // ... etc
} from '@/types/api'
```

## 🚀 Performance

### Otimizações Implementadas

- ✅ **Server-side rendering** (Next.js 14)
- ✅ **Debounce** em inputs de busca
- ✅ **Lazy loading** de componentes
- ✅ **Image optimization** (Next/Image)
- ✅ **CSS purging** (TailwindCSS)
- ✅ **Minificação** automática
- ✅ **Code splitting** por rota

### Métricas Esperadas

- **First Contentful Paint**: < 1s
- **Time to Interactive**: < 2s
- **Lighthouse Score**: > 90

## 🧪 Testes

```bash
# Lint
npm run lint

# Type check
npm run type-check

# Build test
npm run build
```

## 📱 Responsividade

Breakpoints do Tailwind:

- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

Todos os componentes são mobile-first e 100% responsivos.

## 🎯 Próximos Passos

### Features Planejadas

- [ ] Autenticação de usuários
- [ ] Histórico de buscas
- [ ] Favoritos
- [ ] Dark mode
- [ ] Export de resultados (PDF, CSV)
- [ ] Compartilhamento de análises
- [ ] PWA (Progressive Web App)
- [ ] Internacionalização (i18n)

### Melhorias Técnicas

- [ ] Testes unitários (Jest)
- [ ] Testes E2E (Cypress)
- [ ] Storybook para componentes
- [ ] Accessibility audit (a11y)
- [ ] SEO optimization
- [ ] Analytics integration

## 🐛 Troubleshooting

### Erro de conexão com API

```bash
# Verificar se o backend está rodando
curl http://localhost:8000/health

# Verificar variável de ambiente
echo $NEXT_PUBLIC_API_URL
```

### Erros de build

```bash
# Limpar cache do Next.js
rm -rf .next

# Reinstalar dependências
rm -rf node_modules package-lock.json
npm install
```

### TypeScript errors

```bash
# Executar type check
npm run type-check

# Verificar tsconfig.json
```

## 📚 Recursos

### Documentação

- [Next.js](https://nextjs.org/docs)
- [React](https://react.dev)
- [TailwindCSS](https://tailwindcss.com/docs)
- [TypeScript](https://www.typescriptlang.org/docs)

### Componentes

- [Tailwind UI](https://tailwindui.com)
- [Headless UI](https://headlessui.com)
- [Radix UI](https://www.radix-ui.com)

## 👥 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Proprietário - Todos os direitos reservados

---

**Desenvolvido com ⚖️ para revolucionar o acesso à justiça no Brasil**
