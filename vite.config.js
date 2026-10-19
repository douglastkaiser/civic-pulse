import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: process.env.VITE_BASE_PATH || '/civic-pulse/',
  define: {
    __COMMIT_HASH__: JSON.stringify(process.env.GITHUB_SHA?.slice(0, 7) || 'local'),
  },
})
