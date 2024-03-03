<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.main.title')} • Fintasy`,
})
</script>

<template>
  <main h-full flex grow flex-col bg--c-bg-primary p-4 text--c-text>
    {{ $t('example.hello-world') }}
    <a href="/dashboard" text-xl fn-link>
      {{ t('pages.dashboard.title') }}
    </a>
  </main>
</template>

<route lang="yaml">
  meta:
    layout: default
  </route>
