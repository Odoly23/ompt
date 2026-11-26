import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import api from './client'

/**
 * Load an API resource and reload it when the site language changes.
 * `path` may be a string or a function returning one (for route params).
 */
export function useFetch(path, params = () => ({})) {
  const { locale } = useI18n()
  const data = ref(null)
  const loading = ref(true)
  const error = ref(null)

  async function load() {
    loading.value = true
    error.value = null
    try {
      const url = typeof path === 'function' ? path() : path
      data.value = (await api.get(url, { params: params() })).data
    } catch (e) {
      error.value = e.response?.status === 404 ? 'notfound' : 'network'
    } finally {
      loading.value = false
    }
  }

  watch([locale, () => (typeof path === 'function' ? path() : path), () => JSON.stringify(params())], load, { immediate: true })
  return { data, loading, error, reload: load }
}
