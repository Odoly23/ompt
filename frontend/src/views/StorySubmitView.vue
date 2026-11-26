<script setup>
import { reactive, ref } from 'vue'
import api, { apiErrors } from '../api/client'
import { useFetch } from '../api/useFetch'
import PageHead from '../components/PageHead.vue'

const munis = useFetch('municipalities/')
const ERAS = ['1975', 'resistance', 'referendum', 'independence']
const FRONTS = ['armed', 'clandestine', 'diplomatic', 'community', 'other']
const LANGS = [['tet', 'Tetun'], ['pt', 'Português'], ['id', 'Indonesia'], ['en', 'English'], ['other', '…']]

const f = reactive({
  title: '', storyteller: '', nickname: '', municipality: '', era: 'resistance', front: 'community', language: 'tet',
  summary: '', body: '', video_url: '', submitted_by: '', submitter_contact: '', consent: false,
})
const photo = ref(null)
const audio = ref(null)
const errors = ref({})
const busy = ref(false)
const sent = ref(false)

async function submit() {
  busy.value = true
  errors.value = {}
  const fd = new FormData()
  Object.entries(f).forEach(([k, v]) => { if (v !== '' && v !== null) fd.append(k, typeof v === 'boolean' ? String(v) : v) })
  if (photo.value?.files[0]) fd.append('photo', photo.value.files[0])
  if (audio.value?.files[0]) fd.append('audio', audio.value.files[0])
  try {
    await api.post('stories/submit/', fd)
    sent.value = true
    window.scrollTo({ top: 0 })
  } catch (e) {
    errors.value = apiErrors(e)
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <PageHead :title="$t('memoria.form.title')" :lead="$t('memoria.form.lead')" :crumb="{ to: { name: 'memoria' }, label: $t('nav.memoria') }" />
  <section class="section">
    <div class="wrap">
      <div v-if="sent" class="alert ok" role="status">
        <p>{{ $t('memoria.form.thanks') }}</p>
        <RouterLink :to="{ name: 'memoria' }">{{ $t('nav.memoria') }}</RouterLink>
      </div>
      <form v-else class="form wide" novalidate @submit.prevent="submit">
        <p v-if="errors._" class="alert" role="alert">{{ errors._ }}</p>
        <div class="field">
          <label for="s-title">{{ $t('memoria.form.storyTitle') }}</label>
          <input id="s-title" v-model="f.title" required :aria-invalid="!!errors.title" />
          <span v-if="errors.title" class="err">{{ errors.title }}</span>
        </div>
        <div class="form-grid">
          <div class="field">
            <label for="s-teller">{{ $t('memoria.form.storyteller') }}</label>
            <input id="s-teller" v-model="f.storyteller" required :aria-invalid="!!errors.storyteller" />
            <span v-if="errors.storyteller" class="err">{{ errors.storyteller }}</span>
          </div>
          <div class="field">
            <label for="s-nick">{{ $t('memoria.form.nickname') }} <span class="hint">({{ $t('join.optional') }})</span></label>
            <input id="s-nick" v-model="f.nickname" />
          </div>
          <div class="field">
            <label for="s-muni">{{ $t('memoria.form.municipality') }}</label>
            <select id="s-muni" v-model="f.municipality">
              <option value="">{{ $t('join.choose') }}</option>
              <option v-for="m in munis.data.value || []" :key="m.id" :value="m.id">{{ m.name }}</option>
            </select>
          </div>
          <div class="field">
            <label for="s-lang">{{ $t('memoria.lang') }}</label>
            <select id="s-lang" v-model="f.language"><option v-for="[v, l] in LANGS" :key="v" :value="v">{{ l }}</option></select>
          </div>
          <div class="field">
            <label for="s-era">{{ $t('memoria.era') }}</label>
            <select id="s-era" v-model="f.era"><option v-for="e in ERAS" :key="e" :value="e">{{ $t(`memoria.era_.${e}`) }}</option></select>
          </div>
          <div class="field">
            <label for="s-front">{{ $t('memoria.front') }}</label>
            <select id="s-front" v-model="f.front"><option v-for="x in FRONTS" :key="x" :value="x">{{ $t(`memoria.front_.${x}`) }}</option></select>
          </div>
        </div>
        <div class="field">
          <label for="s-sum">{{ $t('memoria.form.summary') }} <span class="hint">({{ $t('join.optional') }})</span></label>
          <input id="s-sum" v-model="f.summary" maxlength="300" />
        </div>
        <div class="field">
          <label for="s-body">{{ $t('memoria.form.body') }}</label>
          <textarea id="s-body" v-model="f.body" required rows="10" aria-describedby="s-body-hint" :aria-invalid="!!errors.body"></textarea>
          <span id="s-body-hint" class="hint">{{ $t('memoria.form.bodyHint') }}</span>
          <span v-if="errors.body" class="err">{{ errors.body }}</span>
        </div>
        <div class="form-grid">
          <div class="field">
            <label for="s-photo">{{ $t('memoria.form.photo') }}</label>
            <input id="s-photo" ref="photo" type="file" accept="image/*" />
            <span v-if="errors.photo" class="err">{{ errors.photo }}</span>
          </div>
          <div class="field">
            <label for="s-audio">{{ $t('memoria.form.audio') }}</label>
            <input id="s-audio" ref="audio" type="file" accept="audio/*" />
            <span v-if="errors.audio" class="err">{{ errors.audio }}</span>
          </div>
        </div>
        <div class="field">
          <label for="s-video">{{ $t('memoria.form.video') }}</label>
          <input id="s-video" v-model="f.video_url" type="url" inputmode="url" />
          <span v-if="errors.video_url" class="err">{{ errors.video_url }}</span>
        </div>
        <fieldset class="you">
          <div class="form-grid">
            <div class="field">
              <label for="s-you">{{ $t('memoria.form.you') }}</label>
              <input id="s-you" v-model="f.submitted_by" required autocomplete="name" :aria-invalid="!!errors.submitted_by" />
              <span v-if="errors.submitted_by" class="err">{{ errors.submitted_by }}</span>
            </div>
            <div class="field">
              <label for="s-contact">{{ $t('memoria.form.contact') }}</label>
              <input id="s-contact" v-model="f.submitter_contact" required aria-describedby="s-contact-hint" :aria-invalid="!!errors.submitter_contact" />
              <span id="s-contact-hint" class="hint">{{ $t('memoria.form.contactHint') }}</span>
              <span v-if="errors.submitter_contact" class="err">{{ errors.submitter_contact }}</span>
            </div>
          </div>
        </fieldset>
        <div class="field">
          <label class="check" for="s-consent">
            <input id="s-consent" v-model="f.consent" type="checkbox" :aria-invalid="!!errors.consent" />
            <span>{{ $t('memoria.form.consent') }}</span>
          </label>
          <span v-if="errors.consent" class="err">{{ errors.consent }}</span>
        </div>
        <div><button class="btn" type="submit" :disabled="busy">{{ busy ? $t('memoria.form.sending') : $t('memoria.form.submit') }}</button></div>
      </form>
    </div>
  </section>
</template>

<style scoped>
.wide { max-width: 820px; }
.you { border: 0; border-top: 2px solid var(--ink); padding: 1rem 0 0; margin: 0.5rem 0 0; }
input[type='file'] { min-height: auto; padding: 0.5rem; }
</style>
