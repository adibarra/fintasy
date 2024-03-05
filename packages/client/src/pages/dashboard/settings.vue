<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.dashboard.settings.title')} • Fintasy`,
})
</script>

<template>
  {{ $t('example.hello-world') }}

  <!-- Some spacers and a temporary footer -->
  <span op-50>
    <div h-10 />
    [ pages/dashboard/settings.vue ]
    <div h-10 />
  </span>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
