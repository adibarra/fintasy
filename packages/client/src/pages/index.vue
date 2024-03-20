<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the main page of the application.
-->

<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.main.title')} • Fintasy`,
})
</script>

<template>
  {{ $t('example.hello-world') }}

  <span>
    Should be a nice landing page. Should describe what the project does and have a link somewhere to login/register.
  </span>
  <a href="/login" text-xl fn-link>
    {{ t('pages.login.title') }}
  </a>
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
