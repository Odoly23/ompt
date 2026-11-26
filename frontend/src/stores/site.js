import { defineStore } from 'pinia'
import api from '../api/client'

export const useSite = defineStore('site', {
  state: () => ({ info: null, stats: null }),
  actions: {
    async load() {
      const [info, stats] = await Promise.allSettled([api.get('site/'), api.get('stats/')])
      if (info.status === 'fulfilled') this.info = info.value.data
      if (stats.status === 'fulfilled') this.stats = stats.value.data
    },
  },
})
