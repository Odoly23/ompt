<script setup>
defineProps({ loading: Boolean, error: [String, null], empty: Boolean })
defineEmits(['retry'])
</script>

<template>
  <p v-if="loading" class="state" role="status">{{ $t('common.loading') }}</p>
  <div v-else-if="error === 'notfound'" class="state">
    <p>{{ $t('common.notFound') }}</p>
    <RouterLink to="/">{{ $t('common.backHome') }}</RouterLink>
  </div>
  <div v-else-if="error" class="state" role="alert">
    <p>{{ $t('common.error') }}</p>
    <button class="btn ghost" type="button" @click="$emit('retry')">{{ $t('common.retry') }}</button>
  </div>
  <p v-else-if="empty" class="state">{{ $t('common.empty') }}</p>
  <slot v-else />
</template>
