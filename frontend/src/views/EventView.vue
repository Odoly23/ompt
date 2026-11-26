<script setup>
import { computed, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import api, { apiErrors } from '../api/client'
import { useFetch } from '../api/useFetch'
import { formatDateTime } from '../i18n'
import { useAuth } from '../stores/auth'
import PageHead from '../components/PageHead.vue'
import LoadState from '../components/LoadState.vue'
import EventDate from '../components/EventDate.vue'

const route = useRoute()
const auth = useAuth()
const ev = useFetch(() => `events/${route.params.slug}/`)
const e = computed(() => ev.data.value)
const guest = reactive({ name: '', phone: '', email: '' })
const busy = ref(false)
const done = ref(false)
const error = ref('')
const apiBase = import.meta.env.VITE_API_URL || ''

const canRegister = computed(() => e.value && !e.value.is_past && e.value.registration_open && e.value.spots_left !== 0)
const isActiveMember = computed(() => auth.member?.status === 'active')

async function register() {
  busy.value = true
  error.value = ''
  try {
    await api.post(`events/${route.params.slug}/register/`, auth.isLoggedIn ? {} : guest)
    done.value = true
    await ev.reload()
  } catch (err) {
    error.value = apiErrors(err)._ || Object.values(apiErrors(err))[0] || ''
  } finally {
    busy.value = false
  }
}
async function cancel() {
  await api.post(`events/${route.params.slug}/cancel/`)
  done.value = false
  await ev.reload()
}
</script>

<template>
  <LoadState :loading="ev.loading.value && !e" :error="ev.error.value" @retry="ev.reload">
    <template v-if="e">
      <PageHead :title="e.title" :crumb="{ to: { name: 'agenda' }, label: $t('nav.agenda') }" />
      <section class="section">
        <div class="wrap detail">
          <div>
            <p v-if="e.is_sample" class="alert warn">{{ $t('common.sampleNote') }}</p>
            <div class="when">
              <EventDate :iso="e.starts_at" :past="e.is_past" />
              <dl>
                <dt>{{ $t('agenda.when') }}</dt>
                <dd>{{ formatDateTime(e.starts_at, undefined, e.time_confirmed) }}<template v-if="e.ends_at"> – {{ formatDateTime(e.ends_at, undefined, e.time_confirmed) }}</template></dd>
                <template v-if="e.location"><dt>{{ $t('agenda.where') }}</dt><dd>{{ e.location }}</dd></template>
              </dl>
            </div>
            <p class="prose desc">{{ e.description }}</p>
            <img v-if="e.image" :src="e.image" alt="" class="cover" />
            <a class="btn ghost" :href="`${apiBase}/api/v1/events/${e.slug}/ics/`">{{ $t('agenda.addCal') }}</a>
          </div>

          <aside class="reg" aria-live="polite">
            <p class="count">{{ $t('agenda.registered', { n: e.registered_count }) }}<template v-if="e.spots_left !== null"> · {{ e.spots_left === 0 ? $t('agenda.full') : $t('agenda.spots', { n: e.spots_left }) }}</template></p>

            <template v-if="e.my_registration">
              <p class="alert ok">{{ e.my_registration.status === 'attended' ? $t('agenda.attended') : $t('agenda.youreIn') }}</p>
              <button v-if="e.my_registration.status === 'registered' && !e.is_past" class="btn ghost" type="button" @click="cancel">{{ $t('agenda.cancel') }}</button>
            </template>
            <p v-else-if="done" class="alert ok">{{ $t('agenda.youreIn') }}</p>
            <p v-else-if="!canRegister" class="alert">{{ e.spots_left === 0 ? $t('agenda.full') : $t('agenda.closed') }}</p>

            <template v-else-if="auth.isLoggedIn">
              <p v-if="e.members_only && !isActiveMember" class="alert">{{ $t('agenda.membersOnly') }}</p>
              <button v-else class="btn" type="button" :disabled="busy" @click="register">{{ busy ? $t('agenda.registering') : $t('agenda.register') }}</button>
            </template>

            <template v-else-if="e.members_only">
              <p>{{ $t('agenda.membersOnly') }}</p>
              <RouterLink class="btn" :to="{ name: 'login', query: { next: route.fullPath } }">{{ $t('agenda.loginToRegister') }}</RouterLink>
            </template>

            <form v-else class="form" @submit.prevent="register">
              <h2>{{ $t('agenda.guestTitle') }}</h2>
              <p class="muted">{{ $t('agenda.guestNote') }} <RouterLink :to="{ name: 'login', query: { next: route.fullPath } }">{{ $t('nav.login') }}</RouterLink></p>
              <div class="field"><label for="g-name">{{ $t('agenda.name') }}</label><input id="g-name" v-model="guest.name" required autocomplete="name" /></div>
              <div class="field"><label for="g-phone">{{ $t('agenda.phone') }}</label><input id="g-phone" v-model="guest.phone" type="tel" autocomplete="tel" /></div>
              <div class="field"><label for="g-email">{{ $t('agenda.email') }}</label><input id="g-email" v-model="guest.email" type="email" autocomplete="email" /></div>
              <div><button class="btn" type="submit" :disabled="busy">{{ busy ? $t('agenda.registering') : $t('agenda.register') }}</button></div>
            </form>
            <p v-if="error" class="alert" role="alert">{{ error }}</p>
          </aside>
        </div>
      </section>
    </template>
  </LoadState>
</template>

<style scoped>
.detail { display: grid; grid-template-columns: 1.5fr 1fr; gap: 3rem; align-items: start; }
.when { display: flex; gap: 1.5rem; align-items: flex-start; margin-bottom: 1.5rem; }
.when dl { margin: 0; display: grid; gap: 0.2rem; }
.when dt { font-size: var(--step--1); color: var(--khaki-dark); }
.when dd { margin: 0 0 0.5rem; font-weight: 700; }
.desc { font-size: var(--step-1); white-space: pre-line; }
.cover { margin: 1.5rem 0; }
.reg { background: var(--paper); border-top: 6px solid var(--red); padding: 1.25rem 1.5rem 1.5rem; position: sticky; top: 1rem; }
.reg h2 { font-size: var(--step-1); margin-bottom: 0.2rem; }
.count { font-weight: 700; }
@media (max-width: 860px) { .detail { grid-template-columns: 1fr; } .reg { position: static; } }
</style>
