import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    id: localStorage.getItem('listener_id')
      ? Number(localStorage.getItem('listener_id'))
      : null,
    username: localStorage.getItem('username') || '',
    loggedIn: !!localStorage.getItem('token'),
  }),
  actions: {
    login(payload: { message: string; listener_id: number; username: string }) {
      this.token = payload.message
      this.id = payload.listener_id
      this.username = payload.username
      this.loggedIn = true
      localStorage.setItem('token', payload.message)
      localStorage.setItem('listener_id', String(payload.listener_id))
      localStorage.setItem('username', payload.username)
    },
    logout() {
      this.token = ''
      this.id = null
      this.username = ''
      this.loggedIn = false
      localStorage.removeItem('token')
      localStorage.removeItem('listener_id')
      localStorage.removeItem('username')
    }
  }
})
