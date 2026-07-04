import { useCallback, useEffect, useState } from 'react'
import type { ReactNode } from 'react'
import * as authApi from '../api/auth'
import { clearToken, getToken, setToken } from '../lib/token'
import type { Credentials, User } from '../types'
import { AuthContext } from './auth-context'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  const refresh = useCallback(async () => {
    setUser(await authApi.getMe())
  }, [])

  // On mount: if a token exists, validate it by fetching the current user.
  // If it's stale, the api interceptor clears it and we fall back to logged-out.
  useEffect(() => {
    async function bootstrap() {
      if (!getToken()) {
        setLoading(false)
        return
      }
      try {
        await refresh()
      } catch {
        clearToken()
      } finally {
        setLoading(false)
      }
    }
    void bootstrap()
  }, [refresh])

  const login = useCallback(
    async (creds: Credentials) => {
      const { access_token } = await authApi.login(creds)
      setToken(access_token)
      await refresh()
    },
    [refresh],
  )

  const register = useCallback(
    async (creds: Credentials) => {
      const { access_token } = await authApi.register(creds)
      setToken(access_token)
      await refresh()
    },
    [refresh],
  )

  const logout = useCallback(() => {
    clearToken()
    setUser(null)
  }, [])

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, refresh }}>
      {children}
    </AuthContext.Provider>
  )
}
