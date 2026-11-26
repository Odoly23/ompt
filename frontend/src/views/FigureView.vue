<script setup>
import { useRoute } from 'vue-router'
import { useFetch } from '../api/useFetch'
import PageHead from '../components/PageHead.vue'
import LoadState from '../components/LoadState.vue'

const route = useRoute()
const fig = useFetch(() => `figures/${route.params.slug}/`)
</script>

<template>
  <LoadState :loading="fig.loading.value" :error="fig.error.value" @retry="fig.reload">
    <template v-if="fig.data.value">
      <PageHead :title="fig.data.value.name" :lead="fig.data.value.role" :crumb="{ to: { name: 'history' }, label: $t('nav.history') }" />
      <section class="section">
        <div class="wrap fig">
          <div class="portrait">
            <img v-if="fig.data.value.photo" :src="fig.data.value.photo" :alt="fig.data.value.name" />
            <span v-else aria-hidden="true">{{ fig.data.value.name.split(' ').slice(0, 2).map((w) => w[0]).join('') }}</span>
          </div>
          <div class="prose">
            <p v-if="fig.data.value.nickname" class="nick">“{{ fig.data.value.nickname }}”</p>
            <p v-if="fig.data.value.birth_year || fig.data.value.death_year" class="years">
              {{ fig.data.value.birth_year || '?' }} – {{ fig.data.value.death_year || '' }}
            </p>
            <p>{{ fig.data.value.bio }}</p>
            <span v-if="fig.data.value.is_sample" class="sample">{{ $t('common.sample') }}</span>
          </div>
        </div>
      </section>
    </template>
  </LoadState>
</template>

<style scoped>
.fig { display: grid; grid-template-columns: 280px 1fr; gap: 2.5rem; align-items: start; }
.portrait { aspect-ratio: 4/5; background: var(--khaki); color: var(--paper); display: grid; place-items: center; }
.portrait img { width: 100%; height: 100%; object-fit: cover; }
.portrait span { font-family: var(--display); font-size: 4rem; }
.nick { font-size: var(--step-2); font-style: italic; margin-bottom: 0.25rem; }
.years { font-weight: 700; }
.prose p:not(.nick):not(.years) { font-size: var(--step-1); }
@media (max-width: 700px) { .fig { grid-template-columns: 1fr; } .portrait { max-width: 220px; } }
</style>
