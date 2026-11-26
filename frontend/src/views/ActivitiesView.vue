<script setup>
import { ref } from 'vue'
import { useFetch } from '../api/useFetch'
import { items } from '../api/client'
import { formatDate } from '../i18n'
import PageHead from '../components/PageHead.vue'
import LoadState from '../components/LoadState.vue'

const CATS = ['training', 'advocacy', 'socioeconomic', 'commemoration', 'organisation', 'publication']
const cat = ref('')
const q = ref('')
const search = ref('')
const page = ref(1)
const list = useFetch('activities/', () => ({ category: cat.value || undefined, search: search.value || undefined, page: page.value }))

function setCat(c) { cat.value = c; page.value = 1 }
function submit() { search.value = q.value.trim(); page.value = 1 }
</script>

<template>
  <PageHead :title="$t('activities.title')" :lead="$t('activities.lead')" />
  <section class="section">
    <div class="wrap">
      <form class="search" role="search" @submit.prevent="submit">
        <label class="visually-hidden" for="act-q">{{ $t('activities.search') }}</label>
        <input id="act-q" v-model="q" type="search" :placeholder="$t('activities.search')" />
        <button class="btn ghost" type="submit">{{ $t('activities.search') }}</button>
      </form>
      <ul class="chips">
        <li><button type="button" :aria-pressed="cat === ''" @click="setCat('')">{{ $t('common.all') }}</button></li>
        <li v-for="c in CATS" :key="c"><button type="button" :aria-pressed="cat === c" @click="setCat(c)">{{ $t(`activities.cat.${c}`) }}</button></li>
      </ul>

      <LoadState :loading="list.loading.value" :error="list.error.value" :empty="!items(list.data.value).length" @retry="list.reload">
        <ul class="rows" v-reveal.stagger>
          <li v-for="a in items(list.data.value)" :key="a.id" class="row" :class="{ 'with-image': a.image }">
            <span class="row-date">{{ a.date ? formatDate(a.date) : $t('activities.noDate') }}</span>
            <div>
              <h3><RouterLink :to="{ name: 'activity', params: { slug: a.slug } }">{{ a.title }}</RouterLink></h3>
              <p>{{ a.summary }}</p>
              <div class="row-meta">
                <span class="tag">{{ $t(`activities.cat.${a.category}`) }}</span>
                <span class="tag red" v-if="a.status !== 'done'">{{ $t(`activities.status.${a.status}`) }}</span>
                <span v-if="a.location" class="muted">{{ a.location }}</span>
                <span v-if="a.is_sample" class="sample">{{ $t('common.sample') }}</span>
              </div>
            </div>
            <img v-if="a.image" :src="a.image" alt="" loading="lazy" />
          </li>
        </ul>
        <nav v-if="list.data.value?.next || list.data.value?.previous" class="pager" aria-label="Pájina">
          <button class="btn ghost" type="button" :disabled="!list.data.value.previous" @click="page--">‹</button>
          <span>{{ page }}</span>
          <button class="btn ghost" type="button" :disabled="!list.data.value.next" @click="page++">›</button>
        </nav>
      </LoadState>
    </div>
  </section>
</template>

<style scoped>
.search { display: flex; gap: 0.5rem; margin-bottom: 1.25rem; max-width: 560px; }
.search input { flex: 1; font: inherit; padding: 0.6rem 0.75rem; min-height: 48px; border: 2px solid var(--line); background: #fff; border-radius: 2px; }
.pager { display: flex; gap: 1rem; align-items: center; margin-top: 1.5rem; }
</style>
