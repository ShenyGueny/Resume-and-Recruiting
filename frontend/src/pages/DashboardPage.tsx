import { useAuth } from '../hooks/useAuth'

// Placeholder landing for authenticated users. Sprint 3 follow-on commits
// replace this with the Kanban board, profile editor, and tailor modal.
export function DashboardPage() {
  const { user, logout } = useAuth()

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-4">
        <h1 className="text-lg font-semibold text-slate-900">Resume &amp; Recruiting</h1>
        <div className="flex items-center gap-4 text-sm">
          <span className="text-slate-500">{user?.email}</span>
          <button
            onClick={logout}
            className="rounded-lg border border-slate-300 px-3 py-1.5 font-medium text-slate-700 transition hover:bg-slate-100"
          >
            Sign out
          </button>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-6 py-10">
        <h2 className="text-xl font-semibold text-slate-900">You're signed in 🎉</h2>
        <p className="mt-2 text-slate-600">
          Auth is wired end-to-end. The Kanban board, profile editor, and AI tailor
          modal land in the next commits.
        </p>

        <div className="mt-6 rounded-xl border border-slate-200 bg-white p-5">
          <h3 className="text-sm font-medium text-slate-700">Anthropic API key</h3>
          <p className="mt-1 text-sm text-slate-500">
            {user?.api_key_hint
              ? `Set (${user.api_key_hint})`
              : 'Not set yet — needed to run the AI tailor pipeline.'}
          </p>
        </div>
      </main>
    </div>
  )
}
