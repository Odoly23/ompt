<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'

// Thin reading-progress bar along the top of the window.
const progress = ref(0)
let frame = 0
function update() {
  frame = 0
  const max = document.documentElement.scrollHeight - window.innerHeight
  progress.value = max > 0 ? Math.min(1, window.scrollY / max) : 0
}
const onScroll = () => { if (!frame) frame = requestAnimationFrame(update) }
onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', onScroll)
  update()
})
onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('resize', onScroll)
  cancelAnimationFrame(frame)
})
</script>

<template>
  <div class="progress" aria-hidden="true" :style="{ transform: `scaleX(${progress})` }"></div>
</template>

<style scoped>
.progress {
  position: fixed; top: 0; left: 0; right: 0; height: 4px; z-index: 50;
  background: linear-gradient(90deg, var(--red), var(--yellow));
  transform-origin: 0 50%; pointer-events: none;
}
</style>
