<script setup>
import { useRoute } from 'vue-router'
import { useFetch } from '../api/useFetch'
import { formatDate } from '../i18n'
import PageHead from '../components/PageHead.vue'
import LoadState from '../components/LoadState.vue'

const route = useRoute()
const act = useFetch(() => `activities/${route.params.slug}/`)
</script>

<template>
  <LoadState :loading="act.loading.value" :error="act.error.value" @retry="act.reload">
    <template v-if="act.data.value">
      <PageHead :title="act.data.value.title" :lead="act.data.value.summary" :crumb="{ to: { name: 'activities' }, label: $t('nav.activities') }" />
      <section class="section">
        <div class="wrap detail">
          <article class="prose">
            <p v-if="act.data.value.is_sample" class="alert warn">{{ $t('common.sampleNote') }}</p>
            <p>{{ act.data.value.body }}</p>
          </article>
          <aside>
            <dl class="meta">
              <dt>{{ $t('activities.when') }}</dt>
              <dd>{{ act.data.value.date ? formatDate(act.data.value.date) : $t('activities.noDate') }}</dd>
              <template v-if="act.data.value.location"><dt>{{ $t('activities.where') }}</dt><dd>{{ act.data.value.location }}</dd></template>
              <dt>{{ $t('common.category') }}</dt>
              <dd><span class="tag">{{ $t(`activities.cat.${act.data.value.category}`) }}</span> <span class="tag red">{{ $t(`activities.status.${act.data.value.status}`) }}</span></dd>
            </dl>
            <img v-if="act.data.value.image" :src="act.data.value.image" :alt="act.data.value.title" />
          </aside>
        </div>
      </section>
    </template>
  </LoadState>
</template>

<style scoped>
.detail { display: grid; grid-template-columns: 1.5fr 1fr; gap: 3rem; align-items: start; }
.prose p { font-size: var(--step-1); }
.meta { margin: 0 0 1.5rem; display: grid; grid-template-columns: auto 1fr; gap: 0.5rem 1rem; border-top: 2px solid var(--ink); padding-top: 1rem; }
.meta dt { font-weight: 700; }
.meta dd { margin: 0; }
@media (max-width: 800px) { .detail { grid-template-columns: 1fr; } }
</style>
