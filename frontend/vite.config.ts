import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// ADD THIS:
import vuetify from 'vite-plugin-vuetify'

export default defineConfig({
  base: '/Spotitried/',
  plugins: [
    vue(),
    vueDevTools(),
    vuetify({ autoImport: true })  // ADD THIS
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
