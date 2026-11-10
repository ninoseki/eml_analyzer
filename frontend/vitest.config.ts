import { fileURLToPath } from 'node:url'

import { configDefaults, defineConfig, mergeConfig } from 'vitest/config'

import viteConfig from './vite.config.ts'

export default defineConfig((config) =>
  mergeConfig(
    viteConfig(config),
    defineConfig({
      test: {
        environment: 'jsdom',
        deps: { interopDefault: false },
        exclude: [...configDefaults.exclude, 'e2e/**'],
        root: fileURLToPath(new URL('./', import.meta.url)),
      },
    }),
  ),
)
