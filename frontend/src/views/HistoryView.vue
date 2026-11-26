<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useFetch } from '../api/useFetch'
import { formatDate } from '../i18n'
import PageHead from '../components/PageHead.vue'
import LoadState from '../components/LoadState.vue'
import PersonCard from '../components/PersonCard.vue'

const history = useFetch('history/')
const figures = useFetch('figures/')
const mandates = useFetch('secretaries-general/')
const CATS = ['foundation', 'resistance', 'independence', 'organisation', 'achievement']
const cat = ref('')

// Draw the red timeline line as the reader scrolls through it.
const timelineEl = ref(null)
const progress = ref(0)
let frame = 0
function measure() {
  frame = 0
  const el = timelineEl.value
  if (!el) return
  const r = el.getBoundingClientRect()
  const mid = window.innerHeight * 0.6
  progress.value = Math.max(0, Math.min(1, (mid - r.top) / r.height))
}
const onScroll = () => { if (!frame) frame = requestAnimationFrame(measure) }
onMounted(() => { window.addEventListener('scroll', onScroll, { passive: true }); window.addEventListener('resize', onScroll); onScroll() })
onBeforeUnmount(() => { window.removeEventListener('scroll', onScroll); window.removeEventListener('resize', onScroll); cancelAnimationFrame(frame) })

const events = computed(() => (history.data.value || []).filter((e) => !cat.value || e.category === cat.value))
// Group consecutive events by year so the year is printed once.
const byYear = computed(() => {
  const groups = []
  for (const e of events.value) {
    const last = groups[groups.length - 1]
    if (last && last.year === e.year) last.items.push(e)
    else groups.push({ year: e.year, items: [e] })
  }
  return groups
})
</script>

<template>
  <PageHead :title="$t('history.title')" :lead="$t('history.lead')" />

  <section class="section">
    <div class="wrap">
      <ul class="chips" :aria-label="$t('history.filter')">
        <li><button type="button" :aria-pressed="cat === ''" @click="cat = ''">{{ $t('common.all') }}</button></li>
        <li v-for="c in CATS" :key="c">
          <button type="button" :aria-pressed="cat === c" @click="cat = c">{{ $t(`history.cat.${c}`) }}</button>
        </li>
      </ul>

      <LoadState :loading="history.loading.value" :error="history.error.value" :empty="!events.length" @retry="history.reload">
        <div ref="timelineEl" class="timeline-wrap" :style="{ '--p': progress }">
        <div class="t-fill" aria-hidden="true"></div>
        <ol class="timeline" v-reveal.stagger="{ from: 'right', step: 60 }">
          <li v-for="g in byYear" :key="g.year" class="t-year">
            <h2 class="t-label">{{ g.year }}</h2>
            <div class="t-items">
              <article v-for="e in g.items" :key="e.id" class="t-item">
                <p class="t-meta">
                  <span class="tag" :class="{ red: e.category === 'resistance' }">{{ $t(`history.cat.${e.category}`) }}</span>
                  <span v-if="e.date">{{ formatDate(e.date) }}</span>
                </p>
                <h3>{{ e.title }}</h3>
                <p>{{ e.body }}</p>
                <img v-if="e.image" :src="e.image" alt="" loading="lazy" />
              </article>
            </div>
          </li>
        </ol>
        </div>
      </LoadState>
    </div>
  </section>

  <section class="section sg" aria-labelledby="sg-title">
    <div class="wrap">
      <h2 id="sg-title">{{ $t('history.sgList') }}</h2>
      <ol class="sg-list" v-reveal.stagger>
        <li v-for="m in mandates.data.value || []" :key="m.id">
          <span class="sg-n">{{ m.number }}</span>
          <div>
            <h3>
              <RouterLink v-if="m.figure_slug" :to="{ name: 'figure', params: { slug: m.figure_slug } }">{{ m.name }}</RouterLink>
              <template v-else>{{ m.name }}</template>
              <span v-if="m.nickname" class="nick"> “{{ m.nickname }}”</span>
            </h3>
            <p class="period">{{ m.start_year }}{{ m.end_year && m.end_year !== m.start_year ? `–${m.end_year}` : '' }}</p>
            <p>{{ m.note }}</p>
          </div>
        </li>
      </ol>
    </div>
  </section>

  <section class="section" aria-labelledby="fig-title">
    <div class="wrap">
      <h2 id="fig-title">{{ $t('history.figures') }}</h2>
      <div class="people" v-reveal.stagger="{ from: 'scale' }">
        <PersonCard v-for="f in figures.data.value || []" :key="f.id" :name="f.name" :nickname="f.nickname" :role="f.role"
                    :photo="f.photo" :years="f.death_year ? `† ${f.death_year}` : ''" :sample="f.is_sample"
                    :to="{ name: 'figure', params: { slug: f.slug } }" />
      </div>
    </div>
  </section>
</template>

<style scoped>
.timeline-wrap { position: relative; padding-left: 2.75rem; }
.timeline-wrap::before, .t-fill { content: ''; position: absolute; left: 0.75rem; top: 0; bottom: 0; width: 4px; background: var(--line); }
.t-fill { background: var(--red); transform-origin: top; transform: scaleY(var(--p, 0)); }
.timeline { list-style: none; margin: 0; padding: 0; }
.t-year { position: relative; display: grid; grid-template-columns: 8rem 1fr; gap: 1.5rem; border-top: 2px solid var(--ink); padding-block: 1.5rem; }
.t-year::before {
  content: ''; position: absolute; left: calc(-2.75rem + 0.75rem + 2px - 11px); top: 2.1rem;
  width: 22px; height: 22px; border-radius: 50%; box-sizing: border-box;
  background: var(--paper-2); border: 4px solid var(--line); transition: border-color 0.4s 0.3s, background 0.4s 0.3s;
}
.t-year.is-revealed::before { border-color: var(--red); background: var(--yellow); }
.t-label { font-size: 2.6rem; color: var(--red); margin: 0; position: sticky; top: 1rem; align-self: start; }
.t-items { display: grid; gap: 1.75rem; }
.t-item h3 { margin-bottom: 0.4rem; }
.t-item p:last-child { margin-bottom: 0; }
.t-meta { display: flex; gap: 0.75rem; align-items: center; font-size: var(--step--1); color: var(--khaki-dark); margin-bottom: 0.4rem; }
.t-item img { margin-top: 1rem; max-width: 420px; }
@media (max-width: 640px) { .t-year { grid-template-columns: 1fr; gap: 0.5rem; } .t-label { position: static; } .timeline-wrap { padding-left: 2.25rem; } .timeline-wrap::before, .t-fill { left: 0.5rem; } .t-year::before { left: calc(-2.25rem + 0.5rem + 2px - 11px); } }

.sg { background: var(--paper); }
.sg-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 0; }
.sg-list li { display: grid; grid-template-columns: 4rem 1fr; gap: 1rem; padding: 1.1rem 0; border-bottom: 1px solid var(--line); }
.sg-n { font-family: var(--display); font-size: 2.4rem; line-height: 1; color: var(--khaki); }
.sg-list h3 { margin: 0; font-size: var(--step-1); }
.sg-list h3 a { color: var(--ink); }
.nick { font-family: var(--body); font-style: italic; font-size: var(--step-0); }
.period { font-weight: 700; margin: 0.2rem 0; }
.sg-list p:last-child { margin-bottom: 0; }
</style>
