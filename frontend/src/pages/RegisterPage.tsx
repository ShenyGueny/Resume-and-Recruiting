import { useNavigate } from 'react-router-dom'
import { AuthForm } from '../components/AuthForm'
import { useAuth } from '../hooks/useAuth'
import { apiError } from '../lib/api'
import type { Credentials } from '../types'

export function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()

  async function handleRegister(creds: Credentials) {
    try {
      await register(creds)
      navigate('/', { replace: true })
    } catch (err) {
      throw new Error(apiError(err, 'Registration failed'))
    }
  }

  return (
    <AuthForm
      title="Create account"
      submitLabel="Create account"
      onSubmit={handleRegister}
      altPrompt="Already have an account?"
      altLabel="Sign in"
      altTo="/login"
    />
  )
}
