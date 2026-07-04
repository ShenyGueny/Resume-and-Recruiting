import axios from 'axios'
import { getToken, clearToken } from './token'

// Base URL points at the FastAPI backend. Defaults to local dev; override with
// VITE_API_URL at build time for staging/prod (S3 + CloudFront → API on ECS).
const baseURL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export const api = axios.create({ baseURL })

// Attach the JWT as a Bearer token on every request when present.
api.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// On 401, the token is stale/invalid — clear it and bounce to login.
// A full reload is the simplest way to reset all in-memory auth state.
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && getToken()) {
      clearToken()
      if (window.location.pathname !== '/login') {
        window.location.assign('/login')
      }
    }
    return Promise.reject(error)
  },
)

// Normalizes a FastAPI error (which puts messages under `detail`) into a string.
export function apiError(error: unknown, fallback = 'Something went wrong'): string {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail
    if (typeof detail === 'string') return detail
    if (Array.isArray(detail) && detail[0]?.msg) return detail[0].msg
    return error.message || fallback
  }
  return fallback
}
