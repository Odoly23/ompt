<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'

// Horizontal slider built on native scroll-snap: swipe, trackpad and keyboard work out of the box.
defineProps({ label: String })
const track = ref(null)
const atStart = ref(true)
const atEnd = ref(false)

function check() {
  const el = track.value
  if (!el) return
  atStart.value = el.scrollLeft <= 4
  atEnd.value = el.scrollLeft + el.clientWidth >= el.scrollWidth - 4
}
function go(dir) {
  const el = track.value
  const smooth = !window.matchMedia('(prefers-reduced-motion: reduce)').matches
  el.scrollBy({ left: dir * el.clientWidth * 0.85, behavior: smooth ? 'smooth' : 'auto' })
}
let ro
onMounted(async () => {
  await nextTick()
  check()
  ro = new ResizeObserver(check)
  ro.observe(track.value)
})
onBeforeUnmount(() => ro?.disconnect())
defineExpose({ check })
</script>

<template>
  <div class="sslider">
    <div class="controls">
      <button type="button" class="arrow" :disabled="atStart" :aria-label="$t('slider.prev')" @click="go(-1)">‹</button>
      <button type="button" class="arrow" :disabled="atEnd" :aria-label="$t('slider.next')" @click="go(1)">›</button>
    </div>
    <div ref="track" class="track" role="region" :aria-label="label" tabindex="0" @scroll.passive="check">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.sslider { position: relative; }
.controls { display: flex; gap: 0.5rem; justify-content: flex-end; margin: -3.6rem 0 1.25rem; }
.arrow {
  width: 48px; height: 48px; font: 700 1.6rem/1 var(--body); cursor: pointer;
  background: transparent; color: inherit; border: 2px solid currentColor; border-radius: 2px;
}
.arrow:hover:not(:disabled) { background: var(--red); border-color: var(--red); color: #fff; }
.arrow:disabled { opacity: 0.3; cursor: default; }
.track {
  display: grid; grid-auto-flow: column; grid-auto-columns: minmax(260px, 23%); gap: 1.5rem;
  overflow-x: auto; scroll-snap-type: x mandatory; scroll-padding-inline: 0;
  padding-bottom: 1rem; scrollbar-width: thin; scrollbar-color: var(--red) transparent;
}
.track > :deep(*) { scroll-snap-align: start; }
.track:focus-visible { outline-offset: 6px; }
@media (max-width: 900px) { .track { grid-auto-columns: minmax(240px, 72%); } .controls { margin-top: 0; } }
</style>
