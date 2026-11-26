<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { LANGS, setLang } from '../i18n'
import { useAuth } from '../stores/auth'

const { locale } = useI18n()
const auth = useAuth()
const open = ref(false)
const route = useRoute()
watch(() => route.fullPath, () => { open.value = false })

const links = [
  ['about', 'about'], ['history', 'history'], ['leadership', 'leadership'], ['activities', 'activities'],
  ['news', 'news'], ['branches', 'branches'], ['documents', 'documents'], ['gallery', 'gallery'], ['contact', 'contact'],
]
</script>

<template>
  <header class="site-header">
    <div class="tais" aria-hidden="true"></div>
    <div class="bar wrap">
      <RouterLink to="/" class="brand" aria-label="OPMT — Organização Popular da Mulher Timor">
        <img src="/opmt-logo.jpg" alt="" width="52" height="52" />
        <span class="brand-text">
          <span class="brand-mark">OPMT</span>
          <span class="brand-sub">Organização Popular da Mulher Timor</span>
        </span>
      </RouterLink>

      <div class="tools">
        <div class="langs" role="group" :aria-label="$t('nav.language')">
          <button v-for="l in LANGS" :key="l.code" type="button" :lang="l.html"
                  :aria-pressed="locale === l.code" @click="setLang(l.code)">{{ l.short }}</button>
        </div>
        <RouterLink v-if="auth.isLoggedIn" class="btn ghost small" :to="{ name: 'dashboard' }">{{ $t('nav.dashboard') }}</RouterLink>
        <template v-else>
          <RouterLink class="login-link" :to="{ name: 'login' }">{{ $t('nav.login') }}</RouterLink>
          <RouterLink class="btn small" :to="{ name: 'join' }">{{ $t('nav.join') }}</RouterLink>
        </template>
        <button class="menu-btn" type="button" :aria-expanded="open" aria-controls="main-nav" @click="open = !open">
          {{ open ? $t('nav.close') : $t('nav.menu') }}
        </button>
      </div>
    </div>
    <nav id="main-nav" class="nav" :class="{ open }" :aria-label="$t('nav.menu')">
      <ul class="wrap">
        <li v-for="[name, key] in links" :key="name">
          <RouterLink :to="{ name }">{{ $t(`nav.${key}`) }}</RouterLink>
        </li>
      </ul>
    </nav>
  </header>
</template>

<style scoped>
.site-header { background: var(--ink); color: #fff; position: relative; z-index: 10; }
.bar { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding-block: 0.8rem; }
.brand { display: flex; align-items: center; gap: 0.75rem; color: #fff; text-decoration: none; min-width: 0; }
.brand img { border-radius: 50%; background: #fff; flex: none; }
.brand-text { display: grid; line-height: 1.1; min-width: 0; }
.brand-mark { font-family: var(--display); font-size: 1.6rem; letter-spacing: 0.04em; }
.brand-sub { font-size: 0.85rem; color: #cfc8a5; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.tools { display: flex; align-items: center; gap: 0.75rem; }
.langs { display: flex; border: 1.5px solid #5a5545; border-radius: 2px; }
.langs button {
  font: 700 0.85rem/1 var(--body); color: #cfc8a5; background: transparent; border: 0;
  padding: 0 0.6rem; min-height: 40px; min-width: 40px; cursor: pointer;
}
.langs button + button { border-left: 1.5px solid #5a5545; }
.langs button[aria-pressed='true'] { background: var(--paper); color: var(--ink); }
.btn.small { min-height: 40px; padding: 0.45rem 0.9rem; font-size: 1rem; }
.btn.ghost.small { color: #fff; border-color: #fff; }
.btn.ghost.small:hover { background: #fff; color: var(--ink); }
.login-link { color: #fff; font-weight: 700; }
.login-link:hover { color: var(--yellow); }
.menu-btn { display: none; font: 700 1rem var(--body); background: transparent; color: #fff; border: 1.5px solid #fff; min-height: 40px; padding: 0 0.8rem; cursor: pointer; }

.nav { background: var(--paper); color: var(--ink); border-bottom: 1px solid var(--line); }
.nav ul { display: flex; flex-wrap: wrap; gap: 0 1.5rem; list-style: none; margin: 0 auto; }
.nav a { display: block; padding: 0.7rem 0; color: var(--ink); text-decoration: none; font-weight: 500; border-bottom: 3px solid transparent; }
.nav a:hover { border-bottom-color: var(--khaki); }
.nav a.router-link-active { border-bottom-color: var(--red); font-weight: 700; }

@media (max-width: 1000px) {
  .brand-sub { display: none; }
  .login-link, .tools > .btn { display: none; }
  .menu-btn { display: inline-block; }
  .nav { display: none; }
  .nav.open { display: block; }
  .nav ul { flex-direction: column; padding-block: 0.5rem; }
  .nav a { padding: 0.75rem 0; border-bottom: 1px solid var(--line); }
  .nav a.router-link-active { border-bottom-color: var(--line); color: var(--red-dark); }
}
@media (max-width: 520px) {
  .brand-text { display: none; }
  .brand img { width: 46px; height: 46px; }
  .tools { gap: 0.5rem; }
  .langs button { min-width: 38px; padding: 0 0.35rem; }
}
</style>
