<script setup>
import { useSite } from '../stores/site'
import { useAuth } from '../stores/auth'
const site = useSite()
const auth = useAuth()
const year = new Date().getFullYear()
const apiBase = import.meta.env.VITE_API_URL || ''
</script>

<template>
  <footer class="site-footer">
    <div class="tais thick" aria-hidden="true"></div>
    <div class="wrap grid">
      <div>
        <p class="mark">OPMT</p>
        <p>{{ $t('footer.about') }}</p>
        <p v-if="site.info?.address" class="small">{{ site.info.address }}</p>
        <p v-if="site.info?.phone || site.info?.email" class="small">
          <a v-if="site.info.phone" :href="`tel:${site.info.phone}`">{{ site.info.phone }}</a>
          <template v-if="site.info.phone && site.info.email"> · </template>
          <a v-if="site.info.email" :href="`mailto:${site.info.email}`">{{ site.info.email }}</a>
        </p>
      </div>
      <ul class="links">
        <li><RouterLink :to="{ name: 'history' }">{{ $t('nav.history') }}</RouterLink></li>
        <li><RouterLink :to="{ name: 'leadership' }">{{ $t('nav.leadership') }}</RouterLink></li>
        <li><RouterLink :to="{ name: 'memoria' }">{{ $t('nav.memoria') }}</RouterLink></li>
        <li><RouterLink :to="{ name: 'agenda' }">{{ $t('nav.agenda') }}</RouterLink></li>
        <li><RouterLink :to="{ name: 'activities' }">{{ $t('nav.activities') }}</RouterLink></li>
        <li><RouterLink :to="{ name: 'documents' }">{{ $t('nav.documents') }}</RouterLink></li>
        <li><RouterLink :to="{ name: 'contact' }">{{ $t('nav.contact') }}</RouterLink></li>
      </ul>
      <ul class="links">
        <li><RouterLink :to="{ name: 'join' }">{{ $t('nav.join') }}</RouterLink></li>
        <li v-if="!auth.isLoggedIn"><RouterLink :to="{ name: 'login' }">{{ $t('nav.login') }}</RouterLink></li>
        <li v-if="site.info?.facebook"><a :href="site.info.facebook" rel="noopener">Facebook</a></li>
        <li v-if="site.info?.youtube"><a :href="site.info.youtube" rel="noopener">YouTube</a></li>
        <li v-if="auth.user?.is_staff"><a :href="`${apiBase}/panel/`">{{ $t('footer.panel') }}</a></li>
      </ul>
    </div>
    <div class="wrap base">
      <span>© {{ year }} {{ $t('footer.rights') }}</span>
      <span>{{ $t('footer.sources') }}</span>
    </div>
  </footer>
</template>

<style scoped>
.site-footer { background: var(--ink); color: #e9e3c4; }
.grid { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 2rem; padding-block: 2.5rem 1.5rem; }
.mark { font-family: var(--display); font-size: 2rem; color: #fff; margin: 0 0 0.25rem; }
.small { font-size: var(--step--1); }
.links { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.5rem; align-content: start; }
a { color: #fff; }
a:hover { color: var(--yellow); }
.base { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 0.5rem 2rem; padding-block: 1rem 1.5rem; border-top: 1px solid #3a372d; font-size: var(--step--1); color: #b5ae8c; }
@media (max-width: 720px) { .grid { grid-template-columns: 1fr 1fr; } .grid > div { grid-column: 1 / -1; } }
</style>
