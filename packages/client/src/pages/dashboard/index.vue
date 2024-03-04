<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.dashboard.title')} • Fintasy`,
})
</script>

<template>
  {{ $t('example.hello-world') }}
  <span op-50>
    [ pages/dashboard/index.vue ]
  </span>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
