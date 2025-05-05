import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// ✅ Vuetify imports
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import '@mdi/font/css/materialdesignicons.css'  // Optional but recommended

const vuetify = createVuetify()

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vuetify)  // ✅ Add Vuetify

app.mount('#app')
