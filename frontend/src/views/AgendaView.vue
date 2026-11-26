<script setup>
import { ref } from 'vue'
import { useFetch } from '../api/useFetch'
import { items } from '../api/client'
import { formatDateTime } from '../i18n'
import PageHead from '../components/PageHead.vue'
import LoadState from '../components/LoadState.vue'
import EventDate from '../components/EventDate.vue'

const when = ref('upcoming')
const list = useFetch('events/', () => ({ when: when.value }))
</script>

<template>
  <PageHead :title="$t('agenda.title')" :lead="$t('agenda.lead')" />
  <section class="section">
    <div class="wrap">
      <ul class="chips">
        <li><button type="button" :aria-pressed="when === 'upcoming'" @click="when = 'upcoming'">{{ $t('agenda.upcoming') }}</button></li>
        <li><button type="button" :aria-pressed="when === 'past'" @click="when = 'past'">{{ $t('agenda.past') }}</button></li>
      </ul>
      <LoadState :loading="list.loading.value" :error="list.error.value" @retry="list.reload">
        <p v-if="!items(list.data.value).length" class="state">{{ $t('agenda.none') }}</p>
        <ul v-else class="events" v-reveal.stagger>
          <li v-for="e in items(list.data.value)" :key="e.id" class="ev">
            <EventDate :iso="e.starts_at" :past="e.is_past" />
            <div class="ev-body">
              <h2><RouterLink :to="{ name: 'event', params: { slug: e.slug } }">{{ e.title }}</RouterLink></h2>
              <p class="meta">{{ formatDateTime(e.starts_at, undefined, e.time_confirmed) }}<template v-if="e.location"> · {{ e.location }}</template></p>
              <p v-if="e.description" class="desc">{{ e.description }}</p>
              <div class="row-meta">
                <span v-if="e.my_registration" class="tag red">{{ e.my_registration.status === 'attended' ? $t('agenda.attended') : $t('agenda.youreIn') }}</span>
                <span v-if="e.members_only" class="tag">{{ $t('agenda.membersOnly') }}</span>
                <span v-if="e.spots_left === 0" class="tag red">{{ $t('agenda.full') }}</span>
                <span v-else-if="e.spots_left" class="muted">{{ $t('agenda.spots', { n: e.spots_left }) }}</span>
                <span v-if="e.is_sample" class="sample">{{ $t('common.sample') }}</span>
              </div>
            </div>
            <RouterLink v-if="!e.is_past && !e.my_registration" class="btn ghost" :to="{ name: 'event', params: { slug: e.slug } }">{{ $t('agenda.register') }}</RouterLink>
          </li>
        </ul>
      </LoadState>
    </div>
  </section>
</template>

<style scoped>
.events { list-style: none; margin: 0; padding: 0; border-top: 2px solid var(--ink); }
.ev { display: flex; gap: 1.5rem; align-items: flex-start; padding: 1.5rem 0; border-bottom: 1px solid var(--line); }
.ev-body { flex: 1; min-width: 0; }
.ev h2 { font-size: var(--step-2); margin-bottom: 0.3rem; }
.ev h2 a { color: var(--ink); text-decoration: none; }
.ev h2 a:hover { color: var(--red); text-decoration: underline; }
.meta { font-weight: 700; margin-bottom: 0.4rem; }
.desc { color: var(--khaki-dark); margin-bottom: 0.25rem; }
@media (max-width: 640px) { .ev { flex-wrap: wrap; } .ev .btn { width: 100%; } }
</style>
