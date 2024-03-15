<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.dashboard.trade.title')} • Fintasy`,
})
</script>

<template>
  {{ $t('example.hello-world') }}

  <span>
    Should be a nice trading center page. It should look like the wireframe.
  </span>

  <!-- Some spacers and a temporary footer -->
  <span op-50>
    <div h-10 />
    [ pages/dashboard/trade.vue ]
    <div h-10 />
  </span>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
