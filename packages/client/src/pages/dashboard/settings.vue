<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the settings page of the application.
-->

<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.dashboard.settings.title')} • Fintasy`,
})
</script>

<template>
  {{ $t('example.hello-world') }}

  <span>
    Should be a nice settings page. It should look like the wireframe.
  </span>

  <div>
    <LanguageSwitch />
  </div>

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
