<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import QRCode from 'qrcode'
import { useRouter } from 'vue-router'
import api, { apiErrors } from '../api/client'
import { formatDate, formatDateTime } from '../i18n'
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

// Card QR, dues, events and announcements
const overview = ref(null)
const qr = ref('')
async function loadOverview() {
  if (!m.value) return
  try {
    overview.value = (await api.get('auth/overview/')).data
    if (overview.value.card) {
      qr.value = await QRCode.toDataURL(overview.value.card.verify_url, { margin: 1, width: 320, color: { dark: '#1d1b16', light: '#ffffff' } })
    }
  } catch { overview.value = null }
}
onMounted(loadOverview)

/** Save the card as a PNG to keep on the phone. */
async function downloadCard() {
  const W = 1012, H = 638
  const c = document.createElement('canvas')
  c.width = W; c.height = H
  const g = c.getContext('2d')
  g.fillStyle = '#1d1b16'; g.fillRect(0, 0, W, H)
  const stripes = ['#c4161c', '#1d1b16', '#f2b705', '#1d1b16', '#0b7a3b', '#1d1b16']
  const widths = [60, 8, 22, 8, 22, 8]
  for (let x = 0, i = 0; x < W; i++) { g.fillStyle = stripes[i % 6]; g.fillRect(x, 0, widths[i % 6], 22); x += widths[i % 6] }
  const load = (src) => new Promise((ok) => { const im = new Image(); im.onload = () => ok(im); im.onerror = () => ok(null); im.src = src })
  const [logo, code] = await Promise.all([load('/opmt-logo.jpg'), load(qr.value)])
  if (logo) { g.save(); g.beginPath(); g.arc(110, 130, 70, 0, Math.PI * 2); g.fillStyle = '#fff'; g.fill(); g.clip(); g.drawImage(logo, 40, 60, 140, 140); g.restore() }
  g.fillStyle = '#f2b705'; g.font = 'bold 30px "Alegreya Sans", sans-serif'; g.fillText('OPMT · Organização Popular da Mulher Timor', 210, 120)
  g.fillStyle = '#ffffff'; g.font = '56px "Alfa Slab One", Georgia, serif'; g.fillText(m.value.full_name, 60, 330, 560)
  g.font = 'bold 40px "Alegreya Sans", sans-serif'; g.fillText(m.value.member_number || '', 60, 400)
  g.fillStyle = '#cfc8a5'; g.font = '32px "Alegreya Sans", sans-serif'; g.fillText(m.value.municipality_name, 60, 455)
  if (code) { g.fillStyle = '#fff'; g.fillRect(650, 250, 310, 310); g.drawImage(code, 660, 260, 290, 290) }
  const a = document.createElement('a')
  a.href = c.toDataURL('image/png'); a.download = `opmt-${m.value.member_number || 'kartaun'}.png`; a.click()
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

          <!-- Digital member card with QR -->
          <div v-if="m.status === 'active'" class="card" aria-labelledby="card-title">
            <div class="tais" aria-hidden="true"></div>
            <div class="card-body">
              <div class="card-id">
                <img src="/opmt-logo.jpg" alt="" width="64" height="64" />
                <div>
                  <p id="card-title" class="card-org">OPMT · {{ $t('dashboard.card') }}</p>
                  <p class="card-name">{{ m.full_name }}</p>
                  <p class="card-num">{{ m.member_number }}</p>
                  <p class="card-meta">{{ m.municipality_name }}<template v-if="m.approved_at"> · {{ $t('dashboard.since') }} {{ formatDate(m.approved_at.slice(0, 10)) }}</template></p>
                </div>
              </div>
              <img v-if="qr" :src="qr" :alt="`QR ${m.member_number}`" class="qr" width="150" height="150" />
            </div>
          </div>
          <template v-if="m.status === 'active'">
            <p class="muted">{{ $t('dash.qrNote') }}</p>
            <button v-if="qr" class="btn ghost" type="button" @click="downloadCard">{{ $t('dash.download') }}</button>
          </template>

          <dl class="facts">
            <div><dt>{{ $t('dashboard.status') }}</dt><dd>{{ m.status_label }}</dd></div>
            <div v-if="m.member_number"><dt>{{ $t('dashboard.number') }}</dt><dd>{{ m.member_number }}</dd></div>
            <div><dt>{{ $t('join.municipality') }}</dt><dd>{{ m.municipality_name }}<template v-if="m.administrative_post_name">, {{ m.administrative_post_name }}</template></dd></div>
          </dl>
          <RouterLink v-if="m.status === 'active'" :to="{ name: 'documents' }">{{ $t('dashboard.docs') }}</RouterLink>

          <template v-if="overview">
            <section class="block" aria-labelledby="ann-h">
              <h2 id="ann-h">{{ $t('dash.news') }}</h2>
              <p v-if="!overview.announcements.length" class="muted">{{ $t('dash.noNews') }}</p>
              <article v-for="a in overview.announcements" :key="a.id" class="ann">
                <p class="ann-meta">{{ formatDateTime(a.sent_at) }}<template v-if="a.scope"> · {{ a.scope }}</template></p>
                <h3>{{ a.title }}</h3>
                <p class="ann-body">{{ a.body }}</p>
              </article>
            </section>

            <section class="block" aria-labelledby="ev-h">
              <h2 id="ev-h">{{ $t('dash.events') }}</h2>
              <p v-if="!overview.registrations.length" class="muted">{{ $t('dash.noEvents') }} <RouterLink :to="{ name: 'agenda' }">{{ $t('dash.seeAgenda') }}</RouterLink></p>
              <ul v-else class="mini">
                <li v-for="r in overview.registrations" :key="r.id">
                  <RouterLink :to="{ name: 'event', params: { slug: r.event_slug } }">{{ r.event_title }}</RouterLink>
                  <span class="muted"> · {{ formatDateTime(r.starts_at, undefined, r.time_confirmed) }}</span>
                  <span class="tag" :class="{ red: r.status === 'attended' }">{{ r.status === 'attended' ? $t('agenda.attended') : $t('agenda.youreIn') }}</span>
                </li>
              </ul>
            </section>

            <section v-if="m.status === 'active'" class="block" aria-labelledby="dues-h">
              <h2 id="dues-h">{{ $t('dash.dues') }}</h2>
              <p v-if="overview.dues.current_rate" class="muted">{{ $t('dash.duesRate', { amount: overview.dues.current_rate }) }}</p>
              <p v-else class="muted">{{ $t('dash.noRate') }}</p>
              <table v-if="overview.dues.current_rate" class="dues">
                <thead><tr><th scope="col">{{ $t('dash.year') }}</th><th scope="col">{{ $t('dash.due') }}</th><th scope="col">{{ $t('dash.paid') }}</th><th scope="col">{{ $t('dash.outstanding') }}</th></tr></thead>
                <tbody>
                  <tr v-for="y in overview.dues.years" :key="y.year">
                    <th scope="row">{{ y.year }}</th><td>${{ y.due }}</td><td>${{ y.paid }}</td>
                    <td :class="{ owing: Number(y.outstanding) > 0 }">${{ y.outstanding }}</td>
                  </tr>
                </tbody>
              </table>
              <template v-if="overview.dues.payments.length">
                <h3>{{ $t('dash.payments') }}</h3>
                <ul class="mini">
                  <li v-for="(p, i) in overview.dues.payments" :key="i">{{ formatDate(p.paid_on) }} — ${{ p.amount }} ({{ p.year }}) · {{ p.method }}<template v-if="p.receipt_number"> · #{{ p.receipt_number }}</template></li>
                </ul>
              </template>
            </section>
          </template>
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
.card { background: var(--ink); color: var(--paper); max-width: 640px; margin-bottom: 0.75rem; }
.block { margin-top: 2.5rem; border-top: 2px solid var(--ink); padding-top: 1rem; }
.block h2 { font-size: var(--step-2); }
.block h3 { margin: 1rem 0 0.4rem; }
.ann { padding: 0.75rem 0; border-bottom: 1px solid var(--line); }
.ann h3 { margin: 0.1rem 0 0.25rem; }
.ann-meta { font-size: var(--step--1); color: var(--khaki-dark); margin: 0; }
.ann-body { white-space: pre-line; margin: 0; }
.mini { margin: 0; padding-left: 1.1rem; display: grid; gap: 0.5rem; }
.mini .tag { margin-left: 0.4rem; }
.dues { border-collapse: collapse; width: 100%; max-width: 480px; }
.dues th, .dues td { text-align: left; padding: 0.45rem 0.5rem; border-bottom: 1px solid var(--line); }
.dues thead th { border-bottom: 2px solid var(--ink); font-size: var(--step--1); }
.dues .owing { color: var(--red-dark); font-weight: 700; }
.card-body { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 1.1rem; padding: 1.25rem; align-items: center; }
.card-id { display: flex; gap: 1rem; align-items: center; min-width: 0; }
.card-id img { border-radius: 50%; background: #fff; flex: none; }
.qr { background: #fff; padding: 6px; width: 132px; height: 132px; flex: none; }
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
