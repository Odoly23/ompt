<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { useFetch } from '../api/useFetch'
import PageHead from '../components/PageHead.vue'
import LoadState from '../components/LoadState.vue'

const route = useRoute()
const munis = useFetch('municipalities/')
const selected = ref(null)
const mapEl = ref(null)
let map = null
const markers = {}

function select(m, fly = true) {
  selected.value = m
  if (map && fly) map.flyTo([Number(m.latitude), Number(m.longitude)], 10, { duration: 0.6 })
  Object.entries(markers).forEach(([code, mk]) => mk.setStyle(style(code === m.code)))
  history.replaceState(null, '', `#${m.code}`)
}

const style = (active) => ({
  radius: active ? 11 : 8, weight: 3, color: '#1d1b16',
  fillColor: active ? '#c4161c' : '#f2b705', fillOpacity: 1,
})

function buildMap(list) {
  if (!mapEl.value || map) return
  map = L.map(mapEl.value, { scrollWheelZoom: false }).setView([-8.85, 125.9], 8)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 14, attribution: '&copy; OpenStreetMap',
  }).addTo(map)
  list.forEach((m) => {
    const mk = L.circleMarker([Number(m.latitude), Number(m.longitude)], style(false))
      .addTo(map).bindTooltip(m.name).on('click', () => select(m, false))
    markers[m.code] = mk
  })
}

watch(() => munis.data.value, async (list) => {
  if (!list) return
  await nextTick()
  buildMap(list)
  const fromHash = list.find((m) => `#${m.code}` === route.hash)
  if (fromHash && !selected.value) select(fromHash)
})

onMounted(() => { if (munis.data.value) buildMap(munis.data.value) })
onBeforeUnmount(() => { map?.remove(); map = null })
</script>

<template>
  <PageHead :title="$t('branches.title')" :lead="$t('branches.lead')" />
  <section class="section">
    <div class="wrap">
      <LoadState :loading="munis.loading.value" :error="munis.error.value" @retry="munis.reload">
        <div class="layout">
          <div ref="mapEl" class="map" role="region" :aria-label="$t('branches.title')"></div>
          <div class="side">
            <div v-if="selected" class="detail" aria-live="polite">
              <h2>{{ selected.name }}</h2>
              <span v-if="selected.is_sample" class="sample">{{ $t('common.sample') }}</span>
              <dl>
                <dt>{{ $t('branches.coordinator') }}</dt>
                <dd>{{ selected.coordinator || $t('branches.noCoordinator') }}</dd>
                <template v-if="selected.phone"><dt>{{ $t('contact.phone') }}</dt><dd><a :href="`tel:${selected.phone}`">{{ selected.phone }}</a></dd></template>
                <template v-if="selected.members_count"><dt>{{ $t('branches.members') }}</dt><dd>{{ selected.members_count }}</dd></template>
                <template v-if="selected.activities_count"><dt>{{ $t('branches.activities') }}</dt><dd>{{ selected.activities_count }}</dd></template>
              </dl>
              <template v-if="selected.posts.length">
                <h3>{{ $t('branches.posts') }}</h3>
                <ul class="posts">
                  <li v-for="p in selected.posts" :key="p.id">{{ p.name }}<span v-if="p.secretary" class="muted"> — {{ p.secretary }}</span></li>
                </ul>
              </template>
            </div>
            <h2 class="list-title">{{ $t('branches.list') }}</h2>
            <ul class="munis">
              <li v-for="m in munis.data.value || []" :key="m.id" :id="m.code">
                <button type="button" :aria-pressed="selected?.code === m.code" @click="select(m)">{{ m.name }}</button>
              </li>
            </ul>
          </div>
        </div>
      </LoadState>
    </div>
  </section>
</template>

<style scoped>
.layout { display: grid; grid-template-columns: 1.6fr 1fr; gap: 2rem; align-items: start; }
.map { height: 520px; border: 2px solid var(--ink); background: var(--paper); z-index: 0; }
.detail { border-top: 6px solid var(--red); background: #fff; padding: 1rem 1.25rem 1.25rem; margin-bottom: 1.5rem; }
.detail h2 { font-size: var(--step-2); margin-bottom: 0.4rem; }
.detail dl { display: grid; grid-template-columns: auto 1fr; gap: 0.35rem 1rem; margin: 1rem 0; }
.detail dt { font-weight: 700; }
.detail dd { margin: 0; }
.detail h3 { font-family: var(--body); font-weight: 700; font-size: var(--step-0); margin: 0 0 0.3rem; }
.posts { margin: 0; padding-left: 1.1rem; }
.list-title { font-size: var(--step-1); }
.munis { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 0.4rem; }
.munis button { width: 100%; text-align: left; font: 500 var(--step-0) var(--body); padding: 0.5rem 0.7rem; min-height: 44px; background: transparent; border: 1.5px solid var(--line); cursor: pointer; border-radius: 2px; }
.munis button[aria-pressed='true'] { background: var(--ink); color: #fff; border-color: var(--ink); }
@media (max-width: 860px) { .layout { grid-template-columns: 1fr; } .map { height: 360px; } }
</style>
