import axios from 'axios'

const ACCESS = 'opmt.access'
const REFRESH = 'opmt.refresh'

function store() {
  try { return window.localStorage } catch { return null }
}

export const tokens = {
  get access() { return store()?.getItem(ACCESS) || null },
  get refresh() { return store()?.getItem(REFRESH) || null },
  set(access, refresh) {
    const s = store(); if (!s) return
    if (access) s.setItem(ACCESS, access)
    if (refresh) s.setItem(REFRESH, refresh)
  },
  clear() {
    const s = store(); if (!s) return
    s.removeItem(ACCESS); s.removeItem(REFRESH)
  },
}

let currentLang = 'tet'
export function setApiLang(lang) { currentLang = lang }

const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL || ''}/api/v1/`,
  timeout: 20000,
})

api.interceptors.request.use((config) => {
  config.params = { lang: currentLang, ...(config.params || {}) }
  const access = tokens.access
  if (access && !config.skipAuth) config.headers.Authorization = `Bearer ${access}`
  return config
})

// Refresh the access token once when it expires, then retry the request.
let refreshing = null
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config
    const expired = error.response?.status === 401 && tokens.refresh && !original._retry && !original.skipAuth
    if (!expired) return Promise.reject(error)
    original._retry = true
    try {
      refreshing ||= api.post('auth/refresh/', { refresh: tokens.refresh }, { skipAuth: true })
      const { data } = await refreshing
      tokens.set(data.access, data.refresh)
      return api(original)
    } catch (e) {
      tokens.clear()
      window.dispatchEvent(new Event('opmt:logout'))
      return Promise.reject(error)
    } finally {
      refreshing = null
    }
  },
)

/** Turn a DRF error response into { field: message } plus a general message. */
export function apiErrors(error) {
  const data = error?.response?.data
  if (!data || typeof data !== 'object') return { _: null }
  const out = {}
  for (const [k, v] of Object.entries(data)) out[k === 'non_field_errors' || k === 'detail' ? '_' : k] = Array.isArray(v) ? v.join(' ') : String(v)
  return out
}

/** Unwrap paginated or plain list responses. */
export const items = (data) => (Array.isArray(data) ? data : data?.results || [])

export default api
