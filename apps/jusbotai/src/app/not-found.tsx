import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="flex h-screen flex-col items-center justify-center gap-4">
      <h1 className="text-4xl font-bold text-slate-900">404</h1>
      <p className="text-slate-500">Página não encontrada</p>
      <Link href="/" className="btn-primary">
        Voltar ao Dashboard
      </Link>
    </div>
  )
}
