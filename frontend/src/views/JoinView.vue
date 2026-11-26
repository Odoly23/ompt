<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { apiErrors } from '../api/client'
import { useFetch } from '../api/useFetch'
import { LANGS } from '../i18n'
import { useAuth } from '../stores/auth'
import PageHead from '../components/PageHead.vue'

const { locale, t } = useI18n()
const router = useRouter()
const auth = useAuth()
const munis = useFetch('municipalities/')

const form = reactive({
  full_name: '', email: '', phone: '', password: '', birth_date: '', municipality: '',
  administrative_post: '', suco: '', aldeia: '', occupation: '', preferred_language: locale.value, accepts_statutes: false,
})
const errors = ref({})
const busy = ref(false)

const posts = computed(() => (munis.data.value || []).find((m) => m.id === Number(form.municipality))?.posts || [])
watch(() => form.municipality, () => { form.administrative_post = '' })

// Latest allowed birth date: 16 years ago today (Estatutu Art. 6).
const maxBirth = (() => { const d = new Date(); d.setFullYear(d.getFullYear() - 16); return d.toISOString().slice(0, 10) })()

async function submit() {
  busy.value = true
  errors.value = {}
  try {
    await auth.register({
      ...form,
      municipality: Number(form.municipality) || null,
      administrative_post: Number(form.administrative_post) || null,
    })
    router.push({ name: 'dashboard' })
  } catch (e) {
    errors.value = apiErrors(e)
    if (!Object.keys(errors.value).length) errors.value = { _: t('common.error') }
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <PageHead :title="$t('join.title')" :lead="$t('join.lead')" />
  <section class="section">
    <div class="wrap layout">
      <form class="form" novalidate @submit.prevent="submit">
        <p v-if="errors._" class="alert" role="alert">{{ errors._ }}</p>

        <div class="field">
          <label for="j-name">{{ $t('join.fullName') }}</label>
          <input id="j-name" v-model="form.full_name" required autocomplete="name" :aria-invalid="!!errors.full_name" />
          <span v-if="errors.full_name" class="err">{{ errors.full_name }}</span>
        </div>
        <div class="form-grid">
          <div class="field">
            <label for="j-email">{{ $t('join.email') }}</label>
            <input id="j-email" v-model="form.email" type="email" required autocomplete="email" :aria-invalid="!!errors.email" />
            <span v-if="errors.email" class="err">{{ errors.email }}</span>
          </div>
          <div class="field">
            <label for="j-phone">{{ $t('join.phone') }}</label>
            <input id="j-phone" v-model="form.phone" type="tel" required autocomplete="tel" :aria-invalid="!!errors.phone" />
            <span v-if="errors.phone" class="err">{{ errors.phone }}</span>
          </div>
          <div class="field">
            <label for="j-birth">{{ $t('join.birthDate') }}</label>
            <input id="j-birth" v-model="form.birth_date" type="date" required :max="maxBirth" :aria-invalid="!!errors.birth_date" />
            <span v-if="errors.birth_date" class="err">{{ errors.birth_date }}</span>
          </div>
          <div class="field">
            <label for="j-pass">{{ $t('join.password') }}</label>
            <input id="j-pass" v-model="form.password" type="password" required minlength="8" autocomplete="new-password" aria-describedby="j-pass-hint" :aria-invalid="!!errors.password" />
            <span id="j-pass-hint" class="hint">{{ $t('join.passwordHint') }}</span>
            <span v-if="errors.password" class="err">{{ errors.password }}</span>
          </div>
          <div class="field">
            <label for="j-muni">{{ $t('join.municipality') }}</label>
            <select id="j-muni" v-model="form.municipality" required :aria-invalid="!!errors.municipality">
              <option value="" disabled>{{ $t('join.choose') }}</option>
              <option v-for="m in munis.data.value || []" :key="m.id" :value="m.id">{{ m.name }}</option>
            </select>
            <span v-if="errors.municipality" class="err">{{ errors.municipality }}</span>
          </div>
          <div class="field">
            <label for="j-post">{{ $t('join.post') }} <span class="hint">({{ $t('join.optional') }})</span></label>
            <select id="j-post" v-model="form.administrative_post" :disabled="!posts.length">
              <option value="">{{ $t('join.choose') }}</option>
              <option v-for="p in posts" :key="p.id" :value="p.id">{{ p.name }}</option>
            </select>
            <span v-if="errors.administrative_post" class="err">{{ errors.administrative_post }}</span>
          </div>
          <div class="field">
            <label for="j-suco">{{ $t('join.suco') }} <span class="hint">({{ $t('join.optional') }})</span></label>
            <input id="j-suco" v-model="form.suco" />
          </div>
          <div class="field">
            <label for="j-aldeia">{{ $t('join.aldeia') }} <span class="hint">({{ $t('join.optional') }})</span></label>
            <input id="j-aldeia" v-model="form.aldeia" />
          </div>
          <div class="field">
            <label for="j-occ">{{ $t('join.occupation') }} <span class="hint">({{ $t('join.optional') }})</span></label>
            <input id="j-occ" v-model="form.occupation" autocomplete="organization-title" />
          </div>
          <div class="field">
            <label for="j-lang">{{ $t('join.prefLang') }}</label>
            <select id="j-lang" v-model="form.preferred_language">
              <option v-for="l in LANGS" :key="l.code" :value="l.code">{{ $t('langName', {}, { locale: l.code }) }}</option>
            </select>
          </div>
        </div>
        <div class="field">
          <label class="check" for="j-accept">
            <input id="j-accept" v-model="form.accepts_statutes" type="checkbox" required :aria-invalid="!!errors.accepts_statutes" />
            <span>{{ $t('join.accept') }}</span>
          </label>
          <span v-if="errors.accepts_statutes" class="err">{{ errors.accepts_statutes }}</span>
        </div>
        <div class="actions">
          <button class="btn" type="submit" :disabled="busy">{{ busy ? $t('join.submitting') : $t('join.submit') }}</button>
          <span>{{ $t('join.haveAccount') }} <RouterLink :to="{ name: 'login' }">{{ $t('nav.login') }}</RouterLink></span>
        </div>
      </form>

      <aside class="steps">
        <h2>{{ $t('join.steps') }}</h2>
        <ol>
          <li>{{ $t('join.step1') }}</li>
          <li>{{ $t('join.step2') }}</li>
          <li>{{ $t('join.step3') }}</li>
        </ol>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.layout { display: grid; grid-template-columns: 1.7fr 1fr; gap: 3rem; align-items: start; }
.actions { display: flex; flex-wrap: wrap; gap: 1rem 1.5rem; align-items: center; }
.steps { background: var(--paper); border-top: 6px solid var(--red); padding: 1.25rem 1.5rem; position: sticky; top: 1rem; }
.steps h2 { font-size: var(--step-1); }
.steps ol { margin: 0; padding-left: 1.4rem; display: grid; gap: 0.75rem; }
.steps li::marker { font-family: var(--display); color: var(--red); }
@media (max-width: 860px) { .layout { grid-template-columns: 1fr; } .steps { order: -1; position: static; } }
</style>
