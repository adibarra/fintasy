<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the login/register page of the application.
-->

<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.login.title')} • Fintasy`,
})
</script>

<template>
  {{ $t('example.hello-world') }}

  <span>
    Should be a login/register UI. If already authenticated redirect to dashboard.
  </span>
  <a href="/dashboard" text-xl fn-link>
    {{ t('pages.dashboard.title') }}
  </a>

  <!-- Some spacers and a temporary footer -->
  <span op-50>
    <div h-10 />
    [ pages/login.vue ]
    <div h-10 />
  </span>
</template>

<route lang="yaml">
  meta:
    layout: default
  </route>
