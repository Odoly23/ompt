<script setup>
import { reactive, ref } from 'vue'
import api, { apiErrors } from '../api/client'
import { useSite } from '../stores/site'
import PageHead from '../components/PageHead.vue'

const site = useSite()
const form = reactive({ name: '', email: '', phone: '', subject: '', message: '' })
const errors = ref({})
const sent = ref(false)
const busy = ref(false)

async function submit() {
  busy.value = true
  errors.value = {}
  try {
    await api.post('contact/', form)
    sent.value = true
    Object.keys(form).forEach((k) => { form[k] = '' })
  } catch (e) {
    errors.value = apiErrors(e)
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <PageHead :title="$t('contact.title')" :lead="$t('contact.lead')" />
  <section class="section">
    <div class="wrap layout">
      <form class="form" novalidate @submit.prevent="submit">
        <p v-if="sent" class="alert ok" role="status">{{ $t('contact.sent') }}</p>
        <p v-if="errors._" class="alert" role="alert">{{ errors._ }}</p>
        <div class="field">
          <label for="c-name">{{ $t('contact.name') }}</label>
          <input id="c-name" v-model="form.name" required autocomplete="name" :aria-invalid="!!errors.name" />
          <span v-if="errors.name" class="err">{{ errors.name }}</span>
        </div>
        <div class="form-grid">
          <div class="field">
            <label for="c-email">{{ $t('contact.email') }}</label>
            <input id="c-email" v-model="form.email" type="email" autocomplete="email" :aria-invalid="!!errors.email" />
            <span v-if="errors.email" class="err">{{ errors.email }}</span>
          </div>
          <div class="field">
            <label for="c-phone">{{ $t('contact.phone') }}</label>
            <input id="c-phone" v-model="form.phone" type="tel" autocomplete="tel" />
          </div>
        </div>
        <span class="hint muted">{{ $t('contact.contactHint') }}</span>
        <div class="field">
          <label for="c-subject">{{ $t('contact.subject') }}</label>
          <input id="c-subject" v-model="form.subject" required :aria-invalid="!!errors.subject" />
          <span v-if="errors.subject" class="err">{{ errors.subject }}</span>
        </div>
        <div class="field">
          <label for="c-msg">{{ $t('contact.message') }}</label>
          <textarea id="c-msg" v-model="form.message" required :aria-invalid="!!errors.message"></textarea>
          <span v-if="errors.message" class="err">{{ errors.message }}</span>
        </div>
        <div><button class="btn" type="submit" :disabled="busy">{{ $t('common.send') }}</button></div>
      </form>
      <aside v-if="site.info" class="info">
        <h2>{{ $t('contact.address') }}</h2>
        <p>{{ site.info.name }}<br />{{ site.info.address }}</p>
        <p v-if="site.info.phone"><a :href="`tel:${site.info.phone}`">{{ site.info.phone }}</a></p>
        <p v-if="site.info.email"><a :href="`mailto:${site.info.email}`">{{ site.info.email }}</a></p>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.layout { display: grid; grid-template-columns: 1.6fr 1fr; gap: 3rem; align-items: start; }
.info { border-top: 6px solid var(--red); padding-top: 1rem; }
.info h2 { font-size: var(--step-1); }
@media (max-width: 800px) { .layout { grid-template-columns: 1fr; } }
</style>
