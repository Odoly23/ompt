<script setup>
import { computed } from 'vue'
import { useFetch } from '../api/useFetch'
import { useAuth } from '../stores/auth'
import PageHead from '../components/PageHead.vue'
import LoadState from '../components/LoadState.vue'

const auth = useAuth()
const docs = useFetch('documents/')
const isActive = computed(() => auth.member?.status === 'active' || auth.user?.is_staff)
const fileType = (url) => (url || '').split('?')[0].split('.').pop().toUpperCase()
</script>

<template>
  <PageHead :title="$t('documents.title')" :lead="$t('documents.lead')" />
  <section class="section">
    <div class="wrap">
      <p v-if="!isActive" class="alert">{{ $t('documents.membersOnly') }} <RouterLink :to="{ name: 'login' }">{{ $t('nav.login') }}</RouterLink></p>
      <LoadState :loading="docs.loading.value" :error="docs.error.value" :empty="!(docs.data.value || []).length" @retry="docs.reload">
        <ul class="rows">
          <li v-for="d in docs.data.value" :key="d.id" class="row">
            <span class="row-date">{{ d.year || '–' }}</span>
            <div class="doc">
              <div>
                <h3>{{ d.title }}</h3>
                <p>{{ d.description }}</p>
                <div class="row-meta">
                  <span class="tag">{{ $t(`documents.cat.${d.category}`) }}</span>
                  <span v-if="d.language" class="muted">{{ $t('documents.language') }}: {{ d.language }}</span>
                </div>
              </div>
              <a v-if="d.file" class="btn ghost" :href="d.file" target="_blank" rel="noopener">{{ $t('common.download') }} {{ fileType(d.file) }}</a>
              <a v-else-if="d.external_url" class="btn ghost" :href="d.external_url" target="_blank" rel="noopener">{{ $t('common.open') }}</a>
            </div>
          </li>
        </ul>
      </LoadState>
    </div>
  </section>
</template>

<style scoped>
.doc { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-start; gap: 1rem 2rem; }
.doc > div { flex: 1 1 320px; }
</style>
