<script setup>
import { computed } from 'vue'
const props = defineProps({ name: String, nickname: String, role: String, photo: String, years: String, sample: Boolean, unknown: Boolean, to: [Object, String] })
const initials = computed(() => props.unknown ? '?' : (props.name || '?').split(' ').filter(Boolean).slice(0, 2).map((w) => w[0]).join(''))
</script>

<template>
  <article class="person">
    <div class="portrait">
      <img v-if="photo" :src="photo" :alt="name" loading="lazy" />
      <span v-else aria-hidden="true">{{ initials }}</span>
    </div>
    <h3>
      <RouterLink v-if="to" :to="to">{{ name }}</RouterLink>
      <template v-else>{{ name }}</template>
    </h3>
    <p v-if="nickname" class="nick">“{{ nickname }}”</p>
    <p v-if="role" class="role">{{ role }}</p>
    <p v-if="years" class="years">{{ years }}</p>
    <span v-if="sample" class="sample">{{ $t('common.sample') }}</span>
  </article>
</template>

<style scoped>
h3 a { color: var(--ink); text-decoration: none; }
h3 a:hover { color: var(--red); text-decoration: underline; }
.nick { margin: 0; font-style: italic; }
.years { margin: 0; font-weight: 700; }
.sample { align-self: flex-start; }
</style>
