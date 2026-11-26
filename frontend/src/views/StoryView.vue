<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useFetch } from '../api/useFetch'
import PageHead from '../components/PageHead.vue'
import LoadState from '../components/LoadState.vue'

const route = useRoute()
const story = useFetch(() => `stories/${route.params.slug}/`)
const s = computed(() => story.data.value)

// YouTube links become an embedded player; other links open in a new tab.
const youtubeId = computed(() => {
  const url = s.value?.video_url || ''
  const m = url.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|shorts\/))([\w-]{11})/)
  return m ? m[1] : null
})
const LANG_NAMES = { tet: 'Tetun', pt: 'Português', id: 'Indonesia', en: 'English', other: '—' }
</script>

<template>
  <LoadState :loading="story.loading.value" :error="story.error.value" @retry="story.reload">
    <template v-if="s">
      <PageHead :title="s.title" :crumb="{ to: { name: 'memoria' }, label: $t('nav.memoria') }">
        <p class="by">{{ $t('memoria.told') }} {{ s.storyteller }}<template v-if="s.nickname"> “{{ s.nickname }}”</template><template v-if="s.municipality_name"> · {{ s.municipality_name }}</template></p>
      </PageHead>
      <section class="section">
        <div class="wrap layout">
          <article class="prose">
            <p v-if="s.is_sample" class="alert warn">{{ $t('common.sampleNote') }}</p>
            <p v-if="s.summary" class="summary">{{ s.summary }}</p>
            <div v-if="s.audio" class="media">
              <h2 class="mh">{{ $t('memoria.listen') }}</h2>
              <audio :src="s.audio" controls preload="none" class="audio"></audio>
            </div>
            <div v-if="youtubeId" class="media video">
              <iframe :src="`https://www.youtube-nocookie.com/embed/${youtubeId}`" :title="s.title" loading="lazy"
                      allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen></iframe>
            </div>
            <p v-else-if="s.video_url"><a :href="s.video_url" target="_blank" rel="noopener">{{ $t('memoria.watch') }}</a></p>
            <div class="body" :lang="s.language !== 'other' ? s.language : undefined">{{ s.body }}</div>
          </article>
          <aside>
            <img v-if="s.photo" :src="s.photo" :alt="s.storyteller" class="photo" />
            <dl class="facts">
              <dt>{{ $t('memoria.era') }}</dt><dd>{{ $t(`memoria.era_.${s.era}`) }}</dd>
              <dt>{{ $t('memoria.front') }}</dt><dd>{{ $t(`memoria.front_.${s.front}`) }}</dd>
              <dt>{{ $t('memoria.lang') }}</dt><dd>{{ LANG_NAMES[s.language] }}</dd>
            </dl>
            <RouterLink class="btn ghost" :to="{ name: 'story-new' }">{{ $t('memoria.share') }}</RouterLink>
          </aside>
        </div>
      </section>
    </template>
  </LoadState>
</template>

<style scoped>
.by { font-weight: 700; color: var(--ink) !important; margin-top: 0.5rem !important; }
.layout { display: grid; grid-template-columns: 1.6fr 1fr; gap: 3rem; align-items: start; }
.summary { font-size: var(--step-2); line-height: 1.35; color: var(--khaki-dark); }
.body { white-space: pre-line; font-size: var(--step-1); line-height: 1.65; max-width: 66ch; }
.media { margin: 1.5rem 0; }
.mh { font-family: var(--body); font-weight: 700; font-size: var(--step-0); margin-bottom: 0.4rem; }
.audio { width: 100%; }
.video { aspect-ratio: 16/9; }
.video iframe { width: 100%; height: 100%; border: 0; }
.photo { margin-bottom: 1.25rem; }
.facts { display: grid; grid-template-columns: auto 1fr; gap: 0.4rem 1rem; margin: 0 0 1.5rem; border-top: 2px solid var(--ink); padding-top: 1rem; }
.facts dt { font-weight: 700; }
.facts dd { margin: 0; }
@media (max-width: 860px) { .layout { grid-template-columns: 1fr; } }
</style>
