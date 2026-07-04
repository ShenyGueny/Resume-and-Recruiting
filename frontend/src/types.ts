// Mirrors the backend Pydantic schemas (backend/app/schemas).

export interface Token {
  access_token: string
  token_type: string
}

export interface User {
  id: string
  email: string
  api_key_hint: string | null
  created_at: string
}

export interface Credentials {
  email: string
  password: string
}

// Application status enum — matches the backend Kanban states.
export type ApplicationStatus =
  | 'saved'
  | 'applied'
  | 'interviewing'
  | 'rejected'
  | 'offer'
