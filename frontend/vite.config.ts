import { fileURLToPath, URL } from 'node:url'

import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

const env = process.env
const target = env.BACKEND_URL || 'http://localhost:8000/'

const basePath = env.VITE_BASE_PATH || '/'
const apiPath = `${basePath}api`

export default defineConfig({
  base: basePath,
  plugins: [vue()],
  server: {
    allowedHosts: true,
    origin: '',
    proxy: {
      [apiPath]: target
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
