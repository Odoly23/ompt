<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useFetch } from '../api/useFetch'
import { useSite } from '../stores/site'
import heroArt from '../assets/hero-art.jpg'

const INTERVAL = 7000
const { t } = useI18n()
const site = useSite()
const api = useFetch('slides/')

// Slide 0 is the built-in poster design; slides managed in the panel follow it.
const slides = computed(() => [{ id: 'poster', poster: true }, ...(api.data.value || [])])
const current = ref(0)
const playing = ref(true)
const hovering = ref(false)
const focused = ref(false)
const reducedMotion = ref(false)
const years = computed(() => site.stats?.years ?? new Date().getFullYear() - 1975)

let timer = null
const active = computed(() => playing.value && !hovering.value && !focused.value && !reducedMotion.value && slides.value.length > 1)
function schedule() {
  clearTimeout(timer)
  if (active.value) timer = setTimeout(() => go(current.value + 1), INTERVAL)
}
function go(i) {
  const n = slides.value.length
  current.value = ((i % n) + n) % n
  schedule()
}
watch([active, () => slides.value.length], schedule)

const isExternal = (link) => /^https?:\/\//.test(link || '')

// Swipe on touch screens.
let startX = null
const onPointerDown = (e) => { if (e.pointerType !== 'mouse') startX = e.clientX }
function onPointerUp(e) {
  if (startX === null) return
  const dx = e.clientX - startX
  startX = null
  if (Math.abs(dx) > 50) go(current.value + (dx < 0 ? 1 : -1))
}
function onKey(e) {
  if (e.key === 'ArrowRight') { e.preventDefault(); go(current.value + 1) }
  if (e.key === 'ArrowLeft') { e.preventDefault(); go(current.value - 1) }
}

// Gentle parallax on the poster illustration.
const shift = ref(0)
let frame = 0
const onScroll = () => {
  if (frame || reducedMotion.value) return
  frame = requestAnimationFrame(() => { frame = 0; shift.value = Math.min(window.scrollY, 600) * 0.25 })
}

onMounted(() => {
  const mq = window.matchMedia('(prefers-reduced-motion: reduce)')
  reducedMotion.value = mq.matches
  mq.addEventListener?.('change', (e) => { reducedMotion.value = e.matches })
  window.addEventListener('scroll', onScroll, { passive: true })
  schedule()
})
onBeforeUnmount(() => {
  clearTimeout(timer)
  cancelAnimationFrame(frame)
  window.removeEventListener('scroll', onScroll)
})
</script>

<template>
  <section class="hero-slider" aria-roledescription="carousel" :aria-label="t('slider.label')"
           @mouseenter="hovering = true" @mouseleave="hovering = false"
           @focusin="focused = true" @focusout="focused = false"
           @pointerdown="onPointerDown" @pointerup="onPointerUp" @keydown="onKey">
    <div class="stack" aria-live="off">
      <div v-for="(s, i) in slides" :key="s.id" class="slide" :class="[{ current: i === current }, s.poster ? 'poster' : `theme-${s.theme}`]"
           role="group" aria-roledescription="slide" :aria-label="t('slider.position', { n: i + 1, total: slides.length })"
           :aria-hidden="i !== current" :inert="i !== current || undefined">

        <!-- Slide 0: the poster -->
        <template v-if="s.poster">
          <div class="art">
            <img :src="heroArt" alt="" width="1400" height="502" :style="{ transform: `translateY(${shift}px) scale(1.06)` }" />
          </div>
          <div class="rule" aria-hidden="true"></div>
          <div class="wrap body">
            <component :is="i === 0 ? 'h1' : 'h2'" class="hero-title" lang="tet">
              <span class="l1">{{ $t('home.heroTop') }}</span>
              <span class="l2">{{ $t('home.heroLine2') }}</span>
              <span class="l3">{{ $t('home.heroLine3') }}</span>
              <span class="l3">{{ $t('home.heroLine4') }}</span>
            </component>
            <div class="side">
              <p class="lead">{{ $t('home.lead', { years }) }}</p>
              <div class="ctas">
                <RouterLink class="btn" :to="{ name: 'history' }">{{ $t('home.ctaHistory') }}</RouterLink>
                <RouterLink class="btn ghost" :to="{ name: 'join' }">{{ $t('home.ctaJoin') }}</RouterLink>
              </div>
              <dl class="facts">
                <div><dt>{{ $t('home.statFounded') }}</dt><dd>1975</dd></div>
                <div v-if="site.stats"><dt>{{ $t('home.statSG') }}</dt><dd>{{ site.stats.secretaries_general }}</dd></div>
                <div v-if="site.stats"><dt>{{ $t('home.statMunis') }}</dt><dd>{{ site.stats.municipalities }}</dd></div>
              </dl>
            </div>
          </div>
        </template>

        <!-- Slides from the admin panel -->
        <template v-else>
          <div v-if="s.image" class="art photo">
            <img :src="s.image" alt="" loading="lazy" />
          </div>
          <div v-if="s.image" class="rule" aria-hidden="true"></div>
          <div class="wrap body managed">
            <h2 class="slide-title">{{ s.title }}</h2>
            <div class="side">
              <p v-if="s.text" class="lead">{{ s.text }}</p>
              <template v-if="s.link && s.button">
                <a v-if="isExternal(s.link)" class="btn" :href="s.link" rel="noopener">{{ s.button }}</a>
                <RouterLink v-else class="btn" :to="s.link">{{ s.button }}</RouterLink>
              </template>
            </div>
          </div>
        </template>
      </div>
    </div>

    <div v-if="slides.length > 1" class="wrap controls">
      <div class="dots">
        <button v-for="(s, i) in slides" :key="s.id" type="button" class="dot"
                :aria-label="t('slider.goTo', { n: i + 1 })" :aria-current="i === current ? 'true' : undefined" @click="go(i)">
          <span :style="i === current && active ? { animationDuration: `${INTERVAL}ms` } : null" :class="{ running: i === current && active }"></span>
        </button>
      </div>
      <div class="buttons">
        <button v-if="!reducedMotion" type="button" class="ctl" :aria-label="playing ? t('slider.pause') : t('slider.play')" :aria-pressed="!playing" @click="playing = !playing">
          <span aria-hidden="true">{{ playing ? '❚❚' : '▶' }}</span>
        </button>
        <button type="button" class="ctl arrow" :aria-label="t('slider.prev')" @click="go(current - 1)">‹</button>
        <button type="button" class="ctl arrow" :aria-label="t('slider.next')" @click="go(current + 1)">›</button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero-slider { background: var(--paper); position: relative; overflow: hidden; touch-action: pan-y; }
.stack { display: grid; }
.slide {
  grid-area: 1 / 1; display: flex; flex-direction: column;
  opacity: 0; visibility: hidden; transform: translateX(2.5%);
  transition: opacity 0.7s ease, transform 0.7s ease, visibility 0s linear 0.7s;
}
.slide.current { opacity: 1; visibility: visible; transform: none; transition: opacity 0.7s ease, transform 0.7s ease, visibility 0s; }

.art { background: #9b9571; overflow: hidden; height: clamp(180px, 40vh, 460px); flex: none; }
.art img { width: 100%; height: 100%; object-fit: cover; object-position: left top; will-change: transform; }
.art.photo img { object-position: center 30%; }
.rule { height: 14px; background: #d51a25; flex: none; }

.body { display: grid; grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr); gap: 2rem 3rem; padding-block: 1.25rem 2rem; align-items: start; flex: 1; }
.hero-title { margin: -0.12em 0 0; font-size: clamp(2.5rem, 6.4vw, 5.6rem); line-height: 0.95; text-transform: uppercase; color: var(--ink); }
.hero-title span { display: block; white-space: nowrap; }
.hero-title .l1 { color: #d51a25; font-size: 1.18em; }
.hero-title .l3 { font-size: 0.66em; line-height: 1.05; }
.side { padding-top: 1rem; }
.lead { font-size: var(--step-1); line-height: 1.45; }
.ctas { display: flex; flex-wrap: wrap; gap: 0.75rem; margin: 1.5rem 0 2rem; }
.facts { display: flex; flex-wrap: wrap; gap: 1.5rem 2.25rem; margin: 0; border-top: 2px solid var(--ink); padding-top: 1rem; }
.facts dt { font-size: var(--step--1); color: var(--khaki-dark); }
.facts dd { margin: 0; font-family: var(--display); font-size: 2rem; line-height: 1.1; }

/* Managed slides */
.managed { align-content: center; padding-block: 2rem 2.5rem; }
.slide-title { font-size: clamp(2.2rem, 5vw, 4.4rem); line-height: 1; margin: 0; }
.managed .btn { margin-top: 0.5rem; }
.slide:not(:has(.art)) .managed { padding-block: clamp(3rem, 10vw, 8rem); }
.theme-ink { background: var(--ink); color: var(--paper); }
.theme-ink .slide-title { color: var(--yellow); }
.theme-ink .btn { background: var(--paper); border-color: var(--paper); color: var(--ink); }
.theme-red { background: #d51a25; color: #fff; }
.theme-red .btn { background: var(--paper); border-color: var(--paper); color: var(--ink); }
.theme-khaki { background: #9b9571; color: var(--ink); }
.theme-paper { background: var(--paper); color: var(--ink); }
.theme-paper .slide-title { color: #d51a25; }

/* Controls */
.controls { display: flex; justify-content: space-between; align-items: center; gap: 1rem; padding-block: 0 1.5rem; position: relative; z-index: 2; }
.dots { display: flex; gap: 0.5rem; }
.dot { width: 44px; height: 44px; padding: 0; background: transparent; border: 0; cursor: pointer; display: grid; place-items: center; }
.dot span { display: block; width: 36px; height: 5px; background: var(--line); position: relative; overflow: hidden; }
.dot span::after { content: ''; position: absolute; inset: 0; background: var(--ink); transform: scaleX(0); transform-origin: left; }
.dot[aria-current='true'] span::after { transform: scaleX(1); }
.dot span.running::after { animation: fill linear forwards; transform: scaleX(0); }
@keyframes fill { to { transform: scaleX(1); } }
.buttons { display: flex; gap: 0.5rem; }
.ctl { min-height: 44px; min-width: 44px; padding: 0 0.6rem; font: 700 var(--step--1) var(--body); background: var(--paper-2); color: var(--ink); border: 2px solid var(--ink); cursor: pointer; border-radius: 2px; }
.ctl.arrow { font-size: 1.5rem; padding: 0; }
.ctl:hover { background: var(--ink); color: #fff; }

@media (max-width: 1000px) {
  .body { grid-template-columns: 1fr; }
  .hero-title { font-size: clamp(2.5rem, 10vw, 5.6rem); }
  .art { height: clamp(150px, 28vh, 300px); }
}
@media (max-width: 480px) {
  .dots { gap: 0; }
  .dot { width: 34px; }
  .dot span { width: 24px; }
}
@media (prefers-reduced-motion: reduce) {
  .slide, .slide.current { transition: none; transform: none; }
}
</style>
