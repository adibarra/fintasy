<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.trade.title')} • Fintasy`,
})
</script>

<template>
  <main h-full flex grow bg--c-bg-primary p-4 text--c-text>
    {{ $t('example.hello-world') }}
  </main>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
