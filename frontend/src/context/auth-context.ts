import { createContext } from 'react'
import type { Credentials, User } from '../types'

export interface AuthContextValue {
  user: User | null
  // True only during the initial "do we have a valid token?" check on load.
  loading: boolean
  login: (creds: Credentials) => Promise<void>
  register: (creds: Credentials) => Promise<void>
  logout: () => void
  // Lets pages (e.g. the API-key form) refresh the cached user after a change.
  refresh: () => Promise<void>
}

export const AuthContext = createContext<AuthContextValue | null>(null)
