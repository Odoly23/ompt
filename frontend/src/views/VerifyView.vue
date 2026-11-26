<script setup>
import { useRoute } from 'vue-router'
import { useFetch } from '../api/useFetch'

// Public page opened by scanning a member card QR with any phone camera.
const route = useRoute()
const res = useFetch(() => `verify/${route.params.token}/`)
</script>

<template>
  <section class="section">
    <div class="wrap">
      <h1 class="visually-hidden">{{ $t('verify.title') }}</h1>
      <p v-if="res.loading.value" class="state" role="status">{{ $t('common.loading') }}</p>
      <div v-else-if="res.error.value || !res.data.value" class="result bad" role="alert">
        <p class="big">✕</p>
        <h2>{{ $t('verify.unknown') }}</h2>
        <p>{{ $t('verify.unknownText') }}</p>
      </div>
      <div v-else class="result" :class="res.data.value.valid ? 'good' : 'warn'">
        <div class="tais" aria-hidden="true"></div>
        <div class="inner">
          <img v-if="res.data.value.photo" :src="res.data.value.photo" alt="" class="ph" />
          <p class="big" aria-hidden="true">{{ res.data.value.valid ? '✓' : '!' }}</p>
          <p class="state-label">{{ res.data.value.valid ? $t('verify.valid') : $t('verify.invalid') }}</p>
          <h2>{{ res.data.value.full_name }}</h2>
          <p class="num">{{ res.data.value.member_number }}</p>
          <p>{{ res.data.value.municipality }}</p>
          <p class="dues">{{ $t('verify.dues') }}: <strong>{{ res.data.value.dues_up_to_date ? $t('verify.duesOk') : $t('verify.duesOwing') }}</strong></p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.result { max-width: 460px; margin: 0 auto; text-align: center; background: #fff; border: 3px solid var(--ink); }
.inner { padding: 1.5rem 1.5rem 2rem; }
.bad { padding: 2rem; border-color: var(--red); }
.big { font-family: var(--display); font-size: 4.5rem; line-height: 1; margin: 0 auto 0.5rem; }
.good .big { color: var(--green); }
.warn .big { color: #b88a00; }
.bad .big { color: var(--red); }
.state-label { font-weight: 700; font-size: var(--step-1); margin: 0 auto; }
.good .state-label { color: var(--green); }
.result h2 { margin: 0.75rem 0 0.25rem; }
.result p { margin-inline: auto; }
.num { font-weight: 700; letter-spacing: 0.05em; }
.ph { width: 120px; height: 120px; object-fit: cover; border-radius: 50%; margin: 0 auto 1rem; }
.dues { border-top: 1px solid var(--line); padding-top: 0.75rem; margin-top: 1rem; }
</style>
