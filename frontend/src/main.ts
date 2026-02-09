import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import '@mdi/font/css/materialdesignicons.css'
import './assets/theme.css'

const vuetify = createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#2a6f6b',
          secondary: '#d98324',
          accent: '#a24c34',
          background: '#f3efe8',
          surface: '#ffffff',
          info: '#4e8bb5',
          success: '#3a7c5c',
          warning: '#c97a1d',
          error: '#c5524a'
        }
      },
      dark: {
        colors: {
          primary: '#6eb8b1',
          secondary: '#f0b26b',
          accent: '#d97757',
          background: '#0f1418',
          surface: '#1c2226',
          info: '#74a9d8',
          success: '#6bb893',
          warning: '#e0a24a',
          error: '#e1736b'
        }
      }
    }
  }
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vuetify)

app.mount('#app')
