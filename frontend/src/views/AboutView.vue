<script setup>
import { computed } from 'vue'
import { useFetch } from '../api/useFetch'
import { useSite } from '../stores/site'
import PageHead from '../components/PageHead.vue'

const site = useSite()
const objectives = useFetch('objectives/', () => ({ kind: 'specific' }))
const organs = useFetch('organs/')
const docs = useFetch('documents/', () => ({ category: 'statute' }))
const statute = computed(() => (docs.data.value || [])[0])
const paragraphs = computed(() => (site.info?.about || '').split('\n\n'))
</script>

<template>
  <PageHead :title="$t('about.title')" :lead="site.info?.tagline" />

  <section class="section">
    <div class="wrap about-grid">
      <div class="prose">
        <p v-for="(p, i) in paragraphs" :key="i" :class="{ first: i === 0 }">{{ p }}</p>
        <a v-if="statute?.file" class="btn ghost" :href="statute.file" target="_blank" rel="noopener">{{ $t('about.statuteLink') }}</a>
      </div>
      <aside class="aside">
        <img src="/opmt-logo.jpg" alt="Logo OPMT" width="320" height="320" />
      </aside>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <h2>{{ $t('about.objectives') }}</h2>
      <ol class="objectives" v-reveal.stagger>
        <li v-for="o in objectives.data.value || []" :key="o.id">{{ o.text }}</li>
      </ol>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <h2>{{ $t('about.organs') }}</h2>
      <dl class="organs" v-reveal.stagger>
        <div v-for="o in organs.data.value || []" :key="o.id">
          <dt>{{ o.name }}</dt>
          <dd>{{ o.description }}</dd>
        </div>
      </dl>
      <h2 class="mt">{{ $t('about.structure') }}</h2>
      <p>{{ $t('about.structureText') }}</p>
      <RouterLink :to="{ name: 'branches' }">{{ $t('nav.branches') }}</RouterLink>
    </div>
  </section>
</template>

<style scoped>
.about-grid { display: grid; grid-template-columns: 1.6fr 1fr; gap: 3rem; align-items: start; }
.prose .first { font-size: var(--step-1); }
.aside img { width: 100%; max-width: 320px; border-radius: 50%; }
.objectives { margin: 0; padding-left: 1.6rem; display: grid; gap: 0.8rem; max-width: 72ch; }
.objectives li::marker { font-family: var(--display); color: var(--red); }
.organs { margin: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem 2.5rem; }
.organs div { border-top: 4px solid var(--ink); padding-top: 0.75rem; }
.organs dt { font-family: var(--display); font-size: var(--step-1); margin-bottom: 0.4rem; }
.organs dd { margin: 0; }
.mt { margin-top: 3rem; }
@media (max-width: 800px) { .about-grid { grid-template-columns: 1fr; } .aside { order: -1; } .aside img { max-width: 180px; } }
</style>
