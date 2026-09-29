import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 3000,
    proxy: {
      // Proxy `/api` to the backend server. Override target with env var API_PROXY_TARGET.
      '/api': {
        target: process.env.API_PROXY_TARGET || 'http://host.docker.internal:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  }
})
