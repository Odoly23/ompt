<script setup>
import { computed } from 'vue'
import { useFetch } from '../api/useFetch'
import { items } from '../api/client'
import { formatDate } from '../i18n'
import { useSite } from '../stores/site'
import PersonCard from '../components/PersonCard.vue'
import heroArt from '../assets/hero-art.jpg'

const site = useSite()
const history = useFetch('history/')
const activities = useFetch('activities/', () => ({ page_size: 4 }))
const figures = useFetch('figures/', () => ({ is_heroine: true }))
const programs = useFetch('programs/')

const KEY_YEARS = [1975, 1999, 2001, 2020, 2025]
const keyMoments = computed(() => {
  const list = history.data.value || []
  return KEY_YEARS.map((y) => list.find((e) => e.year === y && e.category !== 'organisation') || list.find((e) => e.year === y)).filter(Boolean)
})
const years = computed(() => site.stats?.years ?? new Date().getFullYear() - 1975)
const latest = computed(() => items(activities.data.value).slice(0, 4))
</script>

<template>
  <section class="hero" aria-labelledby="hero-title">
    <div class="hero-art">
      <img :src="heroArt" alt="" width="1400" height="502" />
    </div>
    <div class="hero-rule" aria-hidden="true"></div>
    <div class="wrap hero-body">
      <h1 id="hero-title" class="hero-title" lang="tet">
        <span class="l1">{{ $t('home.heroTop') }}</span>
        <span class="l2">{{ $t('home.heroLine2') }}</span>
        <span class="l3">{{ $t('home.heroLine3') }}</span>
        <span class="l3">{{ $t('home.heroLine4') }}</span>
      </h1>
      <div class="hero-side">
        <p class="hero-lead">{{ $t('home.lead', { years }) }}</p>
        <div class="hero-ctas">
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
  </section>

  <section class="section today">
    <div class="wrap today-grid">
      <div>
        <h2>{{ $t('home.todayTitle') }}</h2>
        <p v-if="site.info" class="tagline">{{ site.info.tagline }}</p>
        <RouterLink :to="{ name: 'about' }">{{ $t('nav.about') }}</RouterLink>
      </div>
      <blockquote v-if="site.info?.mission" class="mission">
        <p class="mission-label">{{ $t('home.missionTitle') }}</p>
        <p>{{ site.info.mission }}</p>
        <footer>Estatutu OPMT, Art. 4</footer>
      </blockquote>
    </div>
  </section>

  <section class="section moments" aria-labelledby="moments-title">
    <div class="wrap">
      <div class="section-head">
        <h2 id="moments-title">{{ $t('home.timelineTitle') }}</h2>
        <RouterLink :to="{ name: 'history' }">{{ $t('home.timelineMore') }}</RouterLink>
      </div>
      <ol class="moment-list">
        <li v-for="e in keyMoments" :key="e.id">
          <span class="m-year">{{ e.year }}</span>
          <h3>{{ e.title }}</h3>
          <p>{{ e.body }}</p>
        </li>
      </ol>
    </div>
  </section>

  <section class="section" aria-labelledby="act-title">
    <div class="wrap">
      <div class="section-head">
        <h2 id="act-title">{{ $t('home.activitiesTitle') }}</h2>
        <RouterLink :to="{ name: 'activities' }">{{ $t('common.seeAll') }}</RouterLink>
      </div>
      <ul class="rows">
        <li v-for="a in latest" :key="a.id" class="row">
          <span class="row-date">{{ a.date ? formatDate(a.date) : $t('activities.noDate') }}</span>
          <div>
            <h3><RouterLink :to="{ name: 'activity', params: { slug: a.slug } }">{{ a.title }}</RouterLink></h3>
            <p>{{ a.summary }}</p>
            <div class="row-meta">
              <span class="tag">{{ $t(`activities.cat.${a.category}`) }}</span>
              <span v-if="a.location" class="muted">{{ a.location }}</span>
              <span v-if="a.is_sample" class="sample">{{ $t('common.sample') }}</span>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </section>

  <section class="section heroines" aria-labelledby="heroines-title">
    <div class="wrap">
      <h2 id="heroines-title">{{ $t('home.heroinesTitle') }}</h2>
      <p class="muted">{{ $t('home.heroinesLead') }}</p>
      <div class="people">
        <PersonCard v-for="f in figures.data.value || []" :key="f.id" :name="f.name" :nickname="f.nickname"
                    :role="f.role" :photo="f.photo"
                    :years="f.death_year ? `† ${f.death_year}` : ''"
                    :to="{ name: 'figure', params: { slug: f.slug } }" />
      </div>
    </div>
  </section>

  <section class="section" v-if="programs.data.value?.length" aria-labelledby="prog-title">
    <div class="wrap">
      <h2 id="prog-title">{{ $t('home.programsTitle') }}</h2>
      <ul class="programs">
        <li v-for="p in programs.data.value" :key="p.id">
          <h3>{{ p.title }}</h3>
          <p>{{ p.description }}</p>
        </li>
      </ul>
    </div>
  </section>

  <section class="join-band" aria-labelledby="join-title">
    <div class="wrap join-inner">
      <div>
        <h2 id="join-title">{{ $t('home.joinTitle') }}</h2>
        <p>{{ $t('home.joinText') }}</p>
      </div>
      <RouterLink class="btn light" :to="{ name: 'join' }">{{ $t('nav.join') }}</RouterLink>
    </div>
  </section>
</template>

<style scoped>
/* Hero: a reading of OPMT's 2016 exhibition poster — illustration on khaki, a red rule, then the slab-serif stack. */
.hero { background: var(--paper); overflow: hidden; }
.hero-art { background: #9b9571; }
.hero-art img { width: 100%; max-height: 46vh; object-fit: cover; object-position: left top; }
.hero-rule { height: 14px; background: #d51a25; }
.hero-body { display: grid; grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr); gap: 2rem 3rem; padding-block: 1.25rem 3.5rem; align-items: start; }
.hero-title { margin: -0.12em 0 0; font-size: clamp(2.5rem, 6.4vw, 5.6rem); line-height: 0.95; text-transform: uppercase; color: var(--ink); }
.hero-title span { display: block; white-space: nowrap; }
.hero-title .l1 { color: #d51a25; font-size: 1.18em; }
.hero-title .l3 { font-size: 0.66em; line-height: 1.05; }
.hero-side { padding-top: 1rem; }
.hero-lead { font-size: var(--step-1); line-height: 1.45; }
.hero-ctas { display: flex; flex-wrap: wrap; gap: 0.75rem; margin: 1.5rem 0 2rem; }
.facts { display: flex; flex-wrap: wrap; gap: 1.5rem 2.25rem; margin: 0; border-top: 2px solid var(--ink); padding-top: 1rem; }
.facts dt { font-size: var(--step--1); color: var(--khaki-dark); }
.facts dd { margin: 0; font-family: var(--display); font-size: 2rem; line-height: 1.1; }
@media (max-width: 1000px) {
  .hero-body { grid-template-columns: 1fr; }
  .hero-title { font-size: clamp(2.5rem, 10vw, 5.6rem); }
  .hero-art img { max-height: 32vh; }
}

.today { background: var(--paper-2); }
.today-grid { display: grid; grid-template-columns: 1fr 1.4fr; gap: 2rem 4rem; align-items: start; }
.tagline { font-size: var(--step-2); font-weight: 500; line-height: 1.3; color: var(--khaki-dark); }
.mission { margin: 0; padding: 1.5rem 0 0 1.5rem; border-left: 6px solid var(--red); }
.mission p { font-size: var(--step-1); line-height: 1.5; }
.mission .mission-label { font-weight: 700; font-size: var(--step-0); margin-bottom: 0.5rem; }
.mission footer { font-size: var(--step--1); color: var(--khaki-dark); }
@media (max-width: 860px) { .today-grid { grid-template-columns: 1fr; } }

.moments { background: var(--ink); color: var(--paper); }
.moments h2, .moments h3 { color: #fff; }
.moments a { color: var(--yellow); }
.moment-list { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 1.5rem; }
.moment-list li { border-top: 4px solid var(--red); padding-top: 0.75rem; }
.m-year { font-family: var(--display); font-size: 2.2rem; color: var(--yellow); display: block; line-height: 1.1; margin-bottom: 0.4rem; }
.moment-list p { font-size: var(--step--1); color: #d9d3b3; }
@media (max-width: 1000px) { .moment-list { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 560px) { .moment-list { grid-template-columns: 1fr; } }

.heroines { background: var(--paper); }

.programs { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 0 2rem; }
.programs li { border-top: 2px solid var(--ink); padding: 1rem 0 1.25rem; }
.programs p { margin: 0; color: var(--khaki-dark); }

.join-band { background: var(--red); color: #fff; padding-block: clamp(2rem, 5vw, 3rem); }
.join-inner { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 1.5rem; }
.join-band h2 { margin-bottom: 0.3rem; }
.join-band p { margin: 0; }
</style>
