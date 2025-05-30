import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// ✅ Vuetify imports
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import '@mdi/font/css/materialdesignicons.css'  // Optional but recommended

// ✅ Create Vuetify instance with custom dark theme
const vuetify = createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      dark: {
        colors: {
          primary: '#77878B' // your custom dark mode primary
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
