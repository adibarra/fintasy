<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.main.title')} • Fintasy`,
})
</script>

<template>
  {{ $t('example.hello-world') }}
  <a href="/dashboard" text-xl fn-link>
    {{ t('pages.dashboard.title') }}
  </a>
  <span op-50>
    [ pages/index.vue ]
  </span>
</template>

<route lang="yaml">
  meta:
    layout: default
  </route>
