<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.dashboard.title')} • Fintasy`,
})
</script>

<template>
  <main h-full flex grow flex-col bg--c-bg-primary p-4 text--c-text>
    {{ $t('example.hello-world') }}
    <span op-50>
      [ pages/dashboard/index.vue ]
    </span>
  </main>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
