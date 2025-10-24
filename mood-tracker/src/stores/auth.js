import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    username: localStorage.getItem('username') || null
  }),
  
  actions: {
    setAuth(token, username) {
      this.token = token
      this.username = username
      localStorage.setItem('token', token)
      localStorage.setItem('username', username)
    },
    
    logout() {
      this.token = null
      this.username = null
      localStorage.removeItem('token')
      localStorage.removeItem('username')
    }
  },
  
  getters: {
    isAuthenticated: (state) => !!state.token
  }
})
