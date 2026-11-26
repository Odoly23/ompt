<script setup>
import { useRoute } from 'vue-router'
import { useFetch } from '../api/useFetch'
import { formatDate } from '../i18n'
import PageHead from '../components/PageHead.vue'
import LoadState from '../components/LoadState.vue'

const route = useRoute()
const item = useFetch(() => `news/${route.params.slug}/`)
</script>

<template>
  <LoadState :loading="item.loading.value" :error="item.error.value" @retry="item.reload">
    <template v-if="item.data.value">
      <PageHead :title="item.data.value.title" :lead="formatDate(item.data.value.published_at)" :crumb="{ to: { name: 'news' }, label: $t('nav.news') }" />
      <section class="section">
        <article class="wrap prose">
          <p class="excerpt">{{ item.data.value.excerpt }}</p>
          <img v-if="item.data.value.image" :src="item.data.value.image" alt="" class="cover" />
          <p>{{ item.data.value.body }}</p>
        </article>
      </section>
    </template>
  </LoadState>
</template>

<style scoped>
.excerpt { font-size: var(--step-2); font-family: var(--display); line-height: 1.25; color: var(--khaki-dark); }
.cover { margin: 1.5rem 0; }
.prose p:last-child { font-size: var(--step-1); }
</style>
