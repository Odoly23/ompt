<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '../stores/auth'
import PageHead from '../components/PageHead.vue'

const auth = useAuth()
const route = useRoute()
const router = useRouter()
const email = ref('')
const password = ref('')
const failed = ref(false)
const busy = ref(false)

async function submit() {
  busy.value = true
  failed.value = false
  try {
    await auth.login(email.value.trim(), password.value)
    const next = typeof route.query.next === 'string' && route.query.next.startsWith('/') ? route.query.next : '/konta'
    router.push(next)
  } catch {
    failed.value = true
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <PageHead :title="$t('login.title')" />
  <section class="section">
    <div class="wrap">
      <form class="form login" novalidate @submit.prevent="submit">
        <p v-if="failed" class="alert" role="alert">{{ $t('login.failed') }}</p>
        <div class="field">
          <label for="l-email">{{ $t('login.email') }}</label>
          <input id="l-email" v-model="email" type="email" required autocomplete="username" />
        </div>
        <div class="field">
          <label for="l-pass">{{ $t('login.password') }}</label>
          <input id="l-pass" v-model="password" type="password" required autocomplete="current-password" />
        </div>
        <div class="actions">
          <button class="btn" type="submit" :disabled="busy">{{ busy ? $t('login.submitting') : $t('login.submit') }}</button>
          <span>{{ $t('login.noAccount') }} <RouterLink :to="{ name: 'join' }">{{ $t('nav.join') }}</RouterLink></span>
        </div>
      </form>
    </div>
  </section>
</template>

<style scoped>
.login { max-width: 440px; }
.actions { display: flex; flex-wrap: wrap; gap: 1rem 1.5rem; align-items: center; }
</style>
