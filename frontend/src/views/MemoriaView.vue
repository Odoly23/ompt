<script setup>
import { ref } from 'vue'
import { useFetch } from '../api/useFetch'
import { items } from '../api/client'
import PageHead from '../components/PageHead.vue'
import LoadState from '../components/LoadState.vue'

const ERAS = ['1975', 'resistance', 'referendum', 'independence']
const FRONTS = ['armed', 'clandestine', 'diplomatic', 'community']
const era = ref('')
const front = ref('')
const list = useFetch('stories/', () => ({ era: era.value || undefined, front: front.value || undefined }))
</script>

<template>
  <PageHead :title="$t('memoria.title')" :lead="$t('memoria.lead')">
    <RouterLink class="btn share" :to="{ name: 'story-new' }">{{ $t('memoria.share') }}</RouterLink>
  </PageHead>
  <section class="section">
    <div class="wrap">
      <div class="filters">
        <ul class="chips" :aria-label="$t('memoria.era')">
          <li><button type="button" :aria-pressed="era === ''" @click="era = ''">{{ $t('memoria.all') }}</button></li>
          <li v-for="e in ERAS" :key="e"><button type="button" :aria-pressed="era === e" @click="era = e">{{ $t(`memoria.era_.${e}`) }}</button></li>
        </ul>
        <ul class="chips" :aria-label="$t('memoria.front')">
          <li><button type="button" :aria-pressed="front === ''" @click="front = ''">{{ $t('memoria.all') }}</button></li>
          <li v-for="f in FRONTS" :key="f"><button type="button" :aria-pressed="front === f" @click="front = f">{{ $t(`memoria.front_.${f}`) }}</button></li>
        </ul>
      </div>

      <LoadState :loading="list.loading.value" :error="list.error.value" @retry="list.reload">
        <div v-if="!items(list.data.value).length" class="empty">
          <p>{{ $t('memoria.empty') }}</p>
          <RouterLink class="btn" :to="{ name: 'story-new' }">{{ $t('memoria.share') }}</RouterLink>
        </div>
        <div v-else class="stories" v-reveal.stagger>
          <article v-for="s in items(list.data.value)" :key="s.id" class="story" :class="{ featured: s.is_featured }">
            <div class="ph">
              <img v-if="s.photo" :src="s.photo" alt="" loading="lazy" />
              <span v-else aria-hidden="true">“</span>
            </div>
            <div class="txt">
              <p class="kicker">
                <span class="tag">{{ $t(`memoria.era_.${s.era}`) }}</span>
                <span v-if="s.audio" class="tag red">{{ $t('memoria.listen') }}</span>
                <span v-if="s.video_url" class="tag red">{{ $t('memoria.watch') }}</span>
              </p>
              <h2><RouterLink :to="{ name: 'story', params: { slug: s.slug } }">{{ s.title }}</RouterLink></h2>
              <p class="by">{{ $t('memoria.told') }} {{ s.storyteller }}<template v-if="s.nickname"> “{{ s.nickname }}”</template><template v-if="s.municipality_name"> · {{ s.municipality_name }}</template></p>
              <p class="sum">{{ s.summary || s.body.slice(0, 180) + (s.body.length > 180 ? '…' : '') }}</p>
            </div>
          </article>
        </div>
      </LoadState>
    </div>
  </section>
</template>

<style scoped>
.share { margin-top: 1.25rem; }
.filters { display: grid; gap: 0; }
.filters .chips { margin-bottom: 0.75rem; }
.empty { padding: 2rem; background: var(--paper); border-left: 6px solid var(--red); }
.stories { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 2rem 1.75rem; margin-top: 1rem; }
.story { display: grid; grid-template-rows: auto 1fr; border-top: 4px solid var(--ink); }
.story.featured { grid-column: span 2; grid-template-columns: 1fr 1fr; grid-template-rows: auto; border-top-color: var(--red); }
.ph { aspect-ratio: 16/10; background: var(--khaki); display: grid; place-items: center; overflow: hidden; }
.ph img { width: 100%; height: 100%; object-fit: cover; }
.ph span { font-family: var(--display); font-size: 6rem; color: var(--paper); line-height: 1; }
.txt { padding-top: 0.9rem; }
.featured .txt { padding: 0.9rem 0 0 1.5rem; }
.kicker { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 0.5rem; }
.story h2 { font-size: var(--step-2); margin-bottom: 0.3rem; }
.story h2 a { color: var(--ink); text-decoration: none; }
.story h2 a:hover { color: var(--red); text-decoration: underline; }
.by { font-weight: 700; margin-bottom: 0.4rem; }
.sum { color: var(--khaki-dark); margin: 0; }
@media (max-width: 760px) { .story.featured { grid-column: auto; grid-template-columns: 1fr; } .featured .txt { padding: 0.9rem 0 0; } }
</style>
