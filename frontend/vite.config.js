import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'build',
  },
  server: {
    proxy: {
      '/post': 'http://localhost:8000',
      '/config.json': 'http://localhost:8000',
    },
  },
})
