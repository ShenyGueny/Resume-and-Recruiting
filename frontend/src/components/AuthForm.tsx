import { useState } from 'react'
import { Link } from 'react-router-dom'
import type { Credentials } from '../types'

interface AuthFormProps {
  title: string
  submitLabel: string
  onSubmit: (creds: Credentials) => Promise<void>
  altPrompt: string
  altLabel: string
  altTo: string
}

// Shared email/password form for both Login and Register. Owns its own field
// state, submission/loading state, and error display; the page supplies the
// submit handler (login vs register) and the cross-link.
export function AuthForm({
  title,
  submitLabel,
  onSubmit,
  altPrompt,
  altLabel,
  altTo,
}: AuthFormProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setSubmitting(true)
    try {
      await onSubmit({ email, password })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 px-4">
      <div className="w-full max-w-sm rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <h1 className="mb-1 text-2xl font-semibold text-slate-900">{title}</h1>
        <p className="mb-6 text-sm text-slate-500">Resume &amp; Recruiting</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Email</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 outline-none focus:border-slate-900"
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Password</label>
            <input
              type="password"
              required
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 outline-none focus:border-slate-900"
            />
          </div>

          {error && (
            <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>
          )}

          <button
            type="submit"
            disabled={submitting}
            className="w-full rounded-lg bg-slate-900 py-2 font-medium text-white transition hover:bg-slate-700 disabled:opacity-50"
          >
            {submitting ? 'Please wait…' : submitLabel}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-slate-500">
          {altPrompt}{' '}
          <Link to={altTo} className="font-medium text-slate-900 underline">
            {altLabel}
          </Link>
        </p>
      </div>
    </div>
  )
}
