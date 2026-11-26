<script setup>
import { computed } from 'vue'
import { useFetch } from '../api/useFetch'
import { items } from '../api/client'
import { formatDate } from '../i18n'
import { useSite } from '../stores/site'
import PersonCard from '../components/PersonCard.vue'
import HeroSlider from '../components/HeroSlider.vue'
import ScrollSlider from '../components/ScrollSlider.vue'

const site = useSite()
const history = useFetch('history/')
const activities = useFetch('activities/', () => ({ page_size: 4 }))
const figures = useFetch('figures/', () => ({ is_heroine: true }))
const programs = useFetch('programs/')

// Every event except internal organisation milestones, in order.
const keyMoments = computed(() => (history.data.value || []).filter((e) => e.category !== 'organisation'))
const latest = computed(() => items(activities.data.value).slice(0, 4))
</script>

<template>
  <HeroSlider />

  <section class="section today">
    <div class="wrap today-grid" v-reveal.stagger>
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
      <div class="section-head" v-reveal>
        <h2 id="moments-title">{{ $t('home.timelineTitle') }}</h2>
        <RouterLink :to="{ name: 'history' }">{{ $t('home.timelineMore') }}</RouterLink>
      </div>
      <ScrollSlider :label="$t('home.timelineTitle')">
        <article v-for="e in keyMoments" :key="e.id" class="moment">
          <span class="m-year">{{ e.year }}</span>
          <h3>{{ e.title }}</h3>
          <p>{{ e.body }}</p>
        </article>
      </ScrollSlider>
    </div>
  </section>

  <section class="section" aria-labelledby="act-title">
    <div class="wrap">
      <div class="section-head">
        <h2 id="act-title">{{ $t('home.activitiesTitle') }}</h2>
        <RouterLink :to="{ name: 'activities' }">{{ $t('common.seeAll') }}</RouterLink>
      </div>
      <ul class="rows" v-reveal.stagger>
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
      <h2 id="heroines-title" v-reveal>{{ $t('home.heroinesTitle') }}</h2>
      <p class="muted">{{ $t('home.heroinesLead') }}</p>
      <div class="people" v-reveal.stagger="{ from: 'scale' }">
        <PersonCard v-for="f in figures.data.value || []" :key="f.id" :name="f.name" :nickname="f.nickname"
                    :role="f.role" :photo="f.photo"
                    :years="f.death_year ? `† ${f.death_year}` : ''"
                    :to="{ name: 'figure', params: { slug: f.slug } }" />
      </div>
    </div>
  </section>

  <section class="section" v-if="programs.data.value?.length" aria-labelledby="prog-title">
    <div class="wrap">
      <h2 id="prog-title" v-reveal>{{ $t('home.programsTitle') }}</h2>
      <ul class="programs" v-reveal.stagger>
        <li v-for="p in programs.data.value" :key="p.id">
          <h3>{{ p.title }}</h3>
          <p>{{ p.description }}</p>
        </li>
      </ul>
    </div>
  </section>

  <section class="join-band" aria-labelledby="join-title">
    <div class="wrap join-inner" v-reveal="{ from: 'left' }">
      <div>
        <h2 id="join-title">{{ $t('home.joinTitle') }}</h2>
        <p>{{ $t('home.joinText') }}</p>
      </div>
      <RouterLink class="btn light" :to="{ name: 'join' }">{{ $t('nav.join') }}</RouterLink>
    </div>
  </section>
</template>

<style scoped>
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
.moment { border-top: 4px solid var(--red); padding-top: 0.75rem; }
.m-year { font-family: var(--display); font-size: 2.2rem; color: var(--yellow); display: block; line-height: 1.1; margin-bottom: 0.4rem; }
.moment p { font-size: var(--step--1); color: #d9d3b3; margin: 0; }
.moments .section-head { padding-right: 7.5rem; }
@media (max-width: 900px) { .moments .section-head { padding-right: 0; } }

.heroines { background: var(--paper); }

.programs { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 0 2rem; }
.programs li { border-top: 2px solid var(--ink); padding: 1rem 0 1.25rem; }
.programs p { margin: 0; color: var(--khaki-dark); }

.join-band { background: var(--red); color: #fff; padding-block: clamp(2rem, 5vw, 3rem); }
.join-inner { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 1.5rem; }
.join-band h2 { margin-bottom: 0.3rem; }
.join-band p { margin: 0; }
</style>
