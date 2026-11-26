import { defineStore } from 'pinia'
import api, { tokens } from '../api/client'

export const useAuth = defineStore('auth', {
  state: () => ({ user: null, ready: false }),
  getters: {
    isLoggedIn: (s) => !!s.user,
    member: (s) => s.user?.member || null,
  },
  actions: {
    async init() {
      if (tokens.access) {
        try { this.user = (await api.get('auth/me/')).data } catch { this.user = null }
      }
      this.ready = true
      window.addEventListener('opmt:logout', () => { this.user = null })
    },
    async login(email, password) {
      const { data } = await api.post('auth/login/', { username: email, password }, { skipAuth: true })
      tokens.set(data.access, data.refresh)
      this.user = data.user
    },
    async register(payload) {
      const { data } = await api.post('auth/register/', payload, { skipAuth: true })
      tokens.set(data.access, data.refresh)
      this.user = data.user
    },
    async refreshMe() {
      this.user = (await api.get('auth/me/')).data
    },
    async logout() {
      try { if (tokens.refresh) await api.post('auth/logout/', { refresh: tokens.refresh }) } catch { /* token already invalid */ }
      tokens.clear()
      this.user = null
    },
  },
})
