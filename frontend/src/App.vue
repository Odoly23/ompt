<script setup>
import { onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import SiteHeader from './components/SiteHeader.vue'
import SiteFooter from './components/SiteFooter.vue'
import { useSite } from './stores/site'

const site = useSite()
const { locale } = useI18n()
onMounted(() => site.load())
watch(locale, () => site.load())
</script>

<template>
  <a class="skip" href="#main">{{ $t('skip') }}</a>
  <SiteHeader />
  <main id="main" tabindex="-1">
    <RouterView />
  </main>
  <SiteFooter />
</template>
