import { useNavigate } from 'react-router-dom'
import { AuthForm } from '../components/AuthForm'
import { useAuth } from '../hooks/useAuth'
import { apiError } from '../lib/api'
import type { Credentials } from '../types'

export function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()

  async function handleLogin(creds: Credentials) {
    try {
      await login(creds)
      navigate('/', { replace: true })
    } catch (err) {
      throw new Error(apiError(err, 'Login failed'))
    }
  }

  return (
    <AuthForm
      title="Sign in"
      submitLabel="Sign in"
      onSubmit={handleLogin}
      altPrompt="No account?"
      altLabel="Create one"
      altTo="/register"
    />
  )
}
