<script setup>
defineProps({ title: String, lead: String, crumb: Object })
</script>

<template>
  <div class="page-head">
    <div class="wrap">
      <RouterLink v-if="crumb" class="crumb" :to="crumb.to">{{ crumb.label }}</RouterLink>
      <h1>{{ title }}</h1>
      <p v-if="lead">{{ lead }}</p>
      <slot />
    </div>
  </div>
</template>
