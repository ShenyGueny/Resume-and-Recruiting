import { api } from '../lib/api'
import type { Credentials, Token, User } from '../types'

// Typed wrappers over the /auth endpoints (backend/app/routers/auth.py).

export async function register(creds: Credentials): Promise<Token> {
  const { data } = await api.post<Token>('/auth/register', creds)
  return data
}

export async function login(creds: Credentials): Promise<Token> {
  const { data } = await api.post<Token>('/auth/login', creds)
  return data
}

export async function getMe(): Promise<User> {
  const { data } = await api.get<User>('/auth/me')
  return data
}

export async function updateApiKey(apiKey: string): Promise<User> {
  const { data } = await api.put<User>('/auth/api-key', { api_key: apiKey })
  return data
}
