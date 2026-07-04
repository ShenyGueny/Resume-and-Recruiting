// Single source of truth for the JWT. Stored in localStorage so the session
// survives page reloads. The plaintext Anthropic API key is NEVER stored here —
// it only ever travels in a request body to PUT /auth/api-key.

const TOKEN_KEY = 'ats_token'

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token)
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY)
}
