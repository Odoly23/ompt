<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import api, { apiErrors } from '../api/client'
import { formatDate } from '../i18n'
import { useAuth } from '../stores/auth'
import PageHead from '../components/PageHead.vue'

const auth = useAuth()
const router = useRouter()
const m = computed(() => auth.member)

const profile = reactive({ phone: '', suco: '', aldeia: '', occupation: '' })
watch(m, (v) => { if (v) Object.keys(profile).forEach((k) => { profile[k] = v[k] || '' }) }, { immediate: true })
const profileMsg = ref('')
const profileErr = ref({})

async function saveProfile() {
  profileMsg.value = ''
  profileErr.value = {}
  try {
    await api.patch('auth/me/', profile)
    await auth.refreshMe()
    profileMsg.value = 'saved'
  } catch (e) { profileErr.value = apiErrors(e) }
}

const pw = reactive({ old_password: '', new_password: '' })
const pwMsg = ref('')
const pwErr = ref({})
async function changePassword() {
  pwMsg.value = ''
  pwErr.value = {}
  try {
    await api.post('auth/change-password/', pw)
    pw.old_password = ''; pw.new_password = ''
    pwMsg.value = 'changed'
  } catch (e) { pwErr.value = apiErrors(e) }
}

async function logout() {
  await auth.logout()
  router.push('/')
}
</script>

<template>
  <PageHead :title="$t('dashboard.title')" :lead="auth.user?.member?.full_name || auth.user?.email">
    <button class="btn ghost logout" type="button" @click="logout">{{ $t('nav.logout') }}</button>
  </PageHead>

  <section class="section">
    <div class="wrap grid">
      <div>
        <template v-if="m">
          <p v-if="m.status === 'pending'" class="alert warn">{{ $t('dashboard.pending') }}</p>
          <p v-else-if="m.status === 'rejected'" class="alert">{{ $t('dashboard.rejected') }} {{ m.status_note }}</p>

          <!-- Digital member card -->
          <div v-if="m.status === 'active'" class="card" aria-labelledby="card-title">
            <div class="tais" aria-hidden="true"></div>
            <div class="card-body">
              <img src="/opmt-logo.jpg" alt="" width="72" height="72" />
              <div>
                <p id="card-title" class="card-org">OPMT · {{ $t('dashboard.card') }}</p>
                <p class="card-name">{{ m.full_name }}</p>
                <p class="card-num">{{ m.member_number }}</p>
                <p class="card-meta">{{ m.municipality_name }}<template v-if="m.approved_at"> · {{ $t('dashboard.since') }} {{ formatDate(m.approved_at.slice(0, 10)) }}</template></p>
              </div>
            </div>
          </div>
          <p v-if="m.status === 'active'" class="muted">{{ $t('dashboard.cardNote') }}</p>

          <dl class="facts">
            <div><dt>{{ $t('dashboard.status') }}</dt><dd>{{ m.status_label }}</dd></div>
            <div v-if="m.member_number"><dt>{{ $t('dashboard.number') }}</dt><dd>{{ m.member_number }}</dd></div>
            <div><dt>{{ $t('join.municipality') }}</dt><dd>{{ m.municipality_name }}<template v-if="m.administrative_post_name">, {{ m.administrative_post_name }}</template></dd></div>
          </dl>
          <RouterLink v-if="m.status === 'active'" :to="{ name: 'documents' }">{{ $t('dashboard.docs') }}</RouterLink>
        </template>
        <p v-else-if="auth.user?.is_staff">
          <a href="/panel/">{{ $t('footer.panel') }}</a>
        </p>
      </div>

      <div class="forms">
        <form v-if="m" class="form" @submit.prevent="saveProfile">
          <h2>{{ $t('dashboard.profile') }}</h2>
          <p v-if="profileMsg" class="alert ok" role="status">{{ $t('dashboard.saved') }}</p>
          <div class="field">
            <label for="d-phone">{{ $t('join.phone') }}</label>
            <input id="d-phone" v-model="profile.phone" type="tel" :aria-invalid="!!profileErr.phone" />
            <span v-if="profileErr.phone" class="err">{{ profileErr.phone }}</span>
          </div>
          <div class="form-grid">
            <div class="field"><label for="d-suco">{{ $t('join.suco') }}</label><input id="d-suco" v-model="profile.suco" /></div>
            <div class="field"><label for="d-aldeia">{{ $t('join.aldeia') }}</label><input id="d-aldeia" v-model="profile.aldeia" /></div>
          </div>
          <div class="field"><label for="d-occ">{{ $t('join.occupation') }}</label><input id="d-occ" v-model="profile.occupation" /></div>
          <div><button class="btn" type="submit">{{ $t('common.save') }}</button></div>
        </form>

        <form class="form" @submit.prevent="changePassword">
          <h2>{{ $t('dashboard.password') }}</h2>
          <p v-if="pwMsg" class="alert ok" role="status">{{ $t('dashboard.changed') }}</p>
          <div class="field">
            <label for="d-old">{{ $t('dashboard.oldPassword') }}</label>
            <input id="d-old" v-model="pw.old_password" type="password" autocomplete="current-password" :aria-invalid="!!pwErr.old_password" />
            <span v-if="pwErr.old_password" class="err">{{ pwErr.old_password }}</span>
          </div>
          <div class="field">
            <label for="d-new">{{ $t('dashboard.newPassword') }}</label>
            <input id="d-new" v-model="pw.new_password" type="password" autocomplete="new-password" :aria-invalid="!!pwErr.new_password" />
            <span class="hint">{{ $t('join.passwordHint') }}</span>
            <span v-if="pwErr.new_password" class="err">{{ pwErr.new_password }}</span>
          </div>
          <div><button class="btn ghost" type="submit">{{ $t('dashboard.password') }}</button></div>
        </form>
      </div>
    </div>
  </section>
</template>

<style scoped>
.logout { margin-top: 1rem; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; align-items: start; }
.forms { display: grid; gap: 3rem; }
.forms h2 { font-size: var(--step-2); margin-bottom: 0; }
.card { background: var(--ink); color: var(--paper); max-width: 440px; margin-bottom: 0.75rem; }
.card-body { display: flex; gap: 1.1rem; padding: 1.25rem; align-items: center; }
.card-body img { border-radius: 50%; background: #fff; flex: none; }
.card-body p { margin: 0; }
.card-org { font-size: var(--step--1); color: var(--yellow); font-weight: 700; }
.card-name { font-family: var(--display); font-size: var(--step-1); color: #fff; line-height: 1.2; margin: 0.2rem 0 !important; }
.card-num { font-weight: 700; letter-spacing: 0.04em; }
.card-meta { font-size: var(--step--1); color: #cfc8a5; }
.facts { margin: 1.5rem 0; display: grid; gap: 0.75rem; }
.facts dt { font-size: var(--step--1); color: var(--khaki-dark); }
.facts dd { margin: 0; font-weight: 700; }
@media (max-width: 860px) { .grid { grid-template-columns: 1fr; } }
</style>
