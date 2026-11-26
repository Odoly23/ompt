<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

// Calendar-leaf date block: day number over month, in Díli time.
const props = defineProps({ iso: String, past: Boolean })
const { locale } = useI18n()
const MONTHS = {
  tet: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
}
const parts = computed(() => {
  const d = new Date(props.iso)
  const [y, m, day] = d.toLocaleDateString('en-CA', { timeZone: 'Asia/Dili' }).split('-').map(Number)
  const loc = { pt: 'pt-PT', id: 'id-ID', en: 'en-GB' }[locale.value]
  const month = loc ? new Date(Date.UTC(y, m - 1, 1)).toLocaleDateString(loc, { month: 'short', timeZone: 'UTC' }).replace('.', '') : MONTHS.tet[m - 1]
  return { day, month, year: y }
})
</script>

<template>
  <div class="leaf" :class="{ past }" aria-hidden="true">
    <span class="m">{{ parts.month }}</span>
    <span class="d">{{ parts.day }}</span>
    <span class="y">{{ parts.year }}</span>
  </div>
</template>

<style scoped>
.leaf { width: 5.5rem; text-align: center; border: 2px solid var(--ink); background: #fff; flex: none; }
.leaf span { display: block; }
.m { background: var(--red); color: #fff; font-weight: 700; text-transform: capitalize; padding: 0.15rem 0; }
.d { font-family: var(--display); font-size: 2.3rem; line-height: 1.1; padding-top: 0.2rem; }
.y { font-size: var(--step--1); color: var(--khaki-dark); padding-bottom: 0.25rem; }
.past .m { background: var(--khaki); }
</style>
