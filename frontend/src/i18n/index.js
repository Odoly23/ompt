import { createI18n } from 'vue-i18n'
import { setApiLang } from '../api/client'
import tet from './locales/tet'
import pt from './locales/pt'
import id from './locales/id'
import en from './locales/en'
import features from './locales/features'

export const LANGS = [
  { code: 'tet', short: 'TET', html: 'tet' },
  { code: 'pt', short: 'PT', html: 'pt' },
  { code: 'id', short: 'ID', html: 'id' },
  { code: 'en', short: 'EN', html: 'en' },
]

function initialLang() {
  try {
    const saved = localStorage.getItem('opmt.lang')
    if (LANGS.some((l) => l.code === saved)) return saved
  } catch { /* storage blocked */ }
  return 'tet'
}

function merge(base, extra) {
  const out = { ...base }
  for (const [k, v] of Object.entries(extra)) {
    out[k] = v && typeof v === 'object' && !Array.isArray(v) && base[k] ? merge(base[k], v) : v
  }
  return out
}

const locale = initialLang()
setApiLang(locale)

export const i18n = createI18n({
  legacy: false,
  locale,
  fallbackLocale: 'tet',
  messages: {
    tet: merge(tet, features.tet), pt: merge(pt, features.pt), id: merge(id, features.id), en: merge(en, features.en),
  },
})

export function setLang(code) {
  i18n.global.locale.value = code
  setApiLang(code)
  document.documentElement.lang = code
  try { localStorage.setItem('opmt.lang', code) } catch { /* ignore */ }
}

const DATE_LOCALES = { tet: 'pt-PT', pt: 'pt-PT', id: 'id-ID', en: 'en-GB' }
const TET_MONTHS = ['janeiru', 'fevereiru', 'marsu', 'abríl', 'maiu', 'juñu', 'jullu', 'agostu', 'setembru', 'outubru', 'novembru', 'dezembru']

/** Format an ISO datetime as date + time in Díli time. */
export function formatDateTime(iso, lang = i18n.global.locale.value, withTime = true) {
  if (!iso) return ''
  const d = new Date(iso)
  const day = d.toLocaleDateString('en-CA', { timeZone: 'Asia/Dili' })
  const time = d.toLocaleTimeString('en-GB', { timeZone: 'Asia/Dili', hour: '2-digit', minute: '2-digit' })
  return withTime ? `${formatDate(day, lang)}, ${time}` : formatDate(day, lang)
}

/** Format an ISO date (YYYY-MM-DD) in the current language. */
export function formatDate(iso, lang = i18n.global.locale.value) {
  if (!iso) return ''
  const [y, m, d] = iso.split('-').map(Number)
  if (lang === 'tet') return `${d} ${TET_MONTHS[m - 1]} ${y}`
  return new Date(Date.UTC(y, m - 1, d)).toLocaleDateString(DATE_LOCALES[lang], { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' })
}
