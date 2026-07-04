import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// Dev server runs on :3000 to match the backend's dev CORS allow-list
// (see backend/app/main.py). API base URL is set via VITE_API_URL.
// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: { port: 3000 },
})
