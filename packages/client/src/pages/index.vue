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

  <!-- Some spacers and a temporary footer -->
  <span op-50>
    <div h-10 />
    [ pages/index.vue ]
    <div h-10 />
  </span>
</template>

<route lang="yaml">
  meta:
    layout: default
  </route>
