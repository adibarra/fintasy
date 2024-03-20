<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the tournaments page of the application.
-->

<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.dashboard.tournaments.title')} • Fintasy`,
})
</script>

<template>
  {{ $t('example.hello-world') }}

  <span>
    Should be a nice tournaments page. It should look like the wireframe.
  </span>

  <!-- Some spacers and a temporary footer -->
  <span op-50>
    <div h-10 />
    [ pages/dashboard/tournaments.vue ]
    <div h-10 />
  </span>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
