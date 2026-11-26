<script setup>
import { useFetch } from '../api/useFetch'
import { items } from '../api/client'
import { formatDate } from '../i18n'
import PageHead from '../components/PageHead.vue'
import LoadState from '../components/LoadState.vue'

const list = useFetch('news/')
</script>

<template>
  <PageHead :title="$t('news.title')" :lead="$t('news.lead')" />
  <section class="section">
    <div class="wrap">
      <LoadState :loading="list.loading.value" :error="list.error.value" :empty="!items(list.data.value).length" @retry="list.reload">
        <ul class="rows">
          <li v-for="n in items(list.data.value)" :key="n.id" class="row" :class="{ 'with-image': n.image }">
            <span class="row-date">{{ formatDate(n.published_at) }}</span>
            <div>
              <h3><RouterLink :to="{ name: 'news-item', params: { slug: n.slug } }">{{ n.title }}</RouterLink></h3>
              <p>{{ n.excerpt }}</p>
              <div class="row-meta" v-if="n.is_sample"><span class="sample">{{ $t('common.sample') }}</span></div>
            </div>
            <img v-if="n.image" :src="n.image" alt="" loading="lazy" />
          </li>
        </ul>
      </LoadState>
    </div>
  </section>
</template>
