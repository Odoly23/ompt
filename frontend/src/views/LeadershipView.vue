<script setup>
import { computed } from 'vue'
import { useFetch } from '../api/useFetch'
import PageHead from '../components/PageHead.vue'
import LoadState from '../components/LoadState.vue'
import PersonCard from '../components/PersonCard.vue'

const leaders = useFetch('leaders/')
const organs = useFetch('organs/')
const munis = useFetch('municipalities/')

const national = computed(() => (leaders.data.value || []).filter((l) => !l.municipality))
const hasVacancy = computed(() => national.value.some((l) => l.organ_code === 'secretaria-geral' && l.is_sample))
const isUnknown = (l) => l.is_sample && /konfirma/i.test(l.name)
const leadersFor = (code) => national.value.filter((l) => l.organ_code === code)
</script>

<template>
  <PageHead :title="$t('leadership.title')" :lead="$t('leadership.lead')" />

  <section class="section">
    <div class="wrap">
      <h2>{{ $t('leadership.current') }}</h2>
      <p v-if="hasVacancy" class="alert warn">{{ $t('leadership.vacancy') }}</p>
      <LoadState :loading="leaders.loading.value" :error="leaders.error.value" :empty="!national.length" @retry="leaders.reload">
        <div class="people">
          <PersonCard v-for="l in national" :key="l.id"
                      :name="isUnknown(l) ? $t('common.toConfirm') : l.name" :unknown="isUnknown(l)"
                      :role="l.position" :photo="l.photo" :sample="l.is_sample" />
        </div>
      </LoadState>
    </div>
  </section>

  <section class="section organs-sec">
    <div class="wrap">
      <h2>{{ $t('leadership.organs') }}</h2>
      <ol class="organ-list">
        <li v-for="o in organs.data.value || []" :key="o.id">
          <h3>{{ o.name }}</h3>
          <p>{{ o.description }}</p>
          <ul v-if="leadersFor(o.code).length" class="names">
            <li v-for="l in leadersFor(o.code)" :key="l.id">{{ l.position }}: <strong>{{ isUnknown(l) ? $t('common.toConfirm') : l.name }}</strong></li>
          </ul>
        </li>
      </ol>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <h2>{{ $t('leadership.coordinators') }}</h2>
      <table class="coord">
        <thead><tr><th scope="col">{{ $t('join.municipality') }}</th><th scope="col">{{ $t('branches.coordinator') }}</th><th scope="col">{{ $t('contact.phone') }}</th></tr></thead>
        <tbody>
          <tr v-for="m in munis.data.value || []" :key="m.id">
            <th scope="row"><RouterLink :to="{ name: 'branches', hash: `#${m.code}` }">{{ m.name }}</RouterLink></th>
            <td>{{ m.coordinator || $t('common.toConfirm') }}</td>
            <td>{{ m.phone || '–' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<style scoped>
.organs-sec { background: var(--paper); }
.organ-list { list-style: none; margin: 0; padding: 0; counter-reset: organ; }
.organ-list > li { counter-increment: organ; display: grid; grid-template-columns: 3.5rem 1fr; column-gap: 1rem; padding: 1.25rem 0; border-top: 2px solid var(--ink); }
.organ-list > li::before { content: counter(organ); font-family: var(--display); font-size: 2rem; color: var(--red); grid-row: span 3; line-height: 1; }
.organ-list h3 { margin-bottom: 0.3rem; }
.organ-list p { margin: 0; }
.names { margin: 0.6rem 0 0; padding-left: 1.1rem; }
.coord { width: 100%; border-collapse: collapse; max-width: 760px; }
.coord th, .coord td { text-align: left; padding: 0.65rem 0.5rem; border-bottom: 1px solid var(--line); }
.coord thead th { border-bottom: 2px solid var(--ink); font-size: var(--step--1); }
</style>
