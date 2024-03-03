<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.dashboard.title')} • Fintasy`,
})
</script>

<template>
  {{ $t('example.hello-world') }}
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
