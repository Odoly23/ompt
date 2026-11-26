<script setup>
import { ref } from 'vue'
import { useFetch } from '../api/useFetch'
import { items } from '../api/client'
import { formatDate } from '../i18n'
import PageHead from '../components/PageHead.vue'
import LoadState from '../components/LoadState.vue'

const albums = useFetch('albums/')
const viewer = ref(null)
const dialog = ref(null)

function open(photo) {
  viewer.value = photo
  dialog.value?.showModal()
}
function close() { dialog.value?.close(); viewer.value = null }
</script>

<template>
  <PageHead :title="$t('gallery.title')" :lead="$t('gallery.lead')" />
  <section class="section">
    <div class="wrap">
      <LoadState :loading="albums.loading.value" :error="albums.error.value" :empty="!items(albums.data.value).length" @retry="albums.reload">
        <section v-for="a in items(albums.data.value)" :key="a.id" class="album">
          <div class="album-head">
            <h2>{{ a.title }}</h2>
            <span class="muted">{{ a.date ? formatDate(a.date) : '' }} · {{ $t('gallery.photos', { n: a.photos_count }) }}</span>
          </div>
          <ul class="grid" v-reveal.stagger="{ from: 'scale' }">
            <li v-for="p in a.photos" :key="p.id">
              <button type="button" class="thumb" @click="open(p)">
                <img :src="p.image" :alt="p.caption || a.title" loading="lazy" />
              </button>
              <p v-if="p.caption" class="cap">{{ p.caption }}</p>
            </li>
          </ul>
        </section>
      </LoadState>
    </div>
  </section>

  <dialog ref="dialog" class="viewer" @close="viewer = null" @click.self="close">
    <figure v-if="viewer">
      <img :src="viewer.image" :alt="viewer.caption" />
      <figcaption>{{ viewer.caption }}</figcaption>
    </figure>
    <button class="btn light" type="button" @click="close">{{ $t('nav.close') }}</button>
  </dialog>
</template>

<style scoped>
.album + .album { margin-top: 3rem; }
.album-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 0.5rem 1.5rem; border-bottom: 2px solid var(--ink); margin-bottom: 1.25rem; }
.album-head h2 { margin: 0 0 0.4rem; font-size: var(--step-2); }
.grid { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 1.25rem; }
.thumb { display: block; padding: 0; border: 0; background: var(--paper); cursor: zoom-in; width: 100%; }
.thumb img { width: 100%; aspect-ratio: 3/4; object-fit: cover; }
.cap { font-size: var(--step--1); margin: 0.4rem 0 0; }
.viewer { border: 0; padding: 1rem; background: var(--ink); color: #fff; max-width: min(92vw, 900px); max-height: 92vh; }
.viewer::backdrop { background: rgba(29, 27, 22, 0.85); }
.viewer img { max-height: 75vh; width: auto; margin: 0 auto; }
.viewer figure { margin: 0 0 1rem; }
.viewer figcaption { margin-top: 0.5rem; }
</style>
