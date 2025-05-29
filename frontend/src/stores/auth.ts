// src/stores/auth.ts
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    loggedIn: !!localStorage.getItem('token'),
  }),
  actions: {
    login(token: string) {
      this.token = token
      this.loggedIn = true
      localStorage.setItem('token', token)
    },
    logout() {
      this.token = ''
      this.loggedIn = false
      localStorage.removeItem('token')
    }
  }
})
