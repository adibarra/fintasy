<!--
  @author: Mariptime (Akshay)
  @description: This component is used to display the login/register page of the application.
-->

<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.main.title')} • Fintasy`,
})
</script>

<template>
  <nav class="flex md:mx-6 md:my-4">
    <router-link to="/" class="flex items-center justify-center gap-2">
      <img
        src="/pwa-192x192.png" alt="Fintasy Logo"
        class="h-14"
      >
      <div class="text-2xl lg:text-4xl md:text-3xl">
        Fintasy
      </div>
    </router-link>
    <div class="grow" />
    <div class="flex items-center gap-5">
      <button
        class="rd-10 bg--c-inverse hover:bg--c-accent px-6 py-2 text--c-bg md:text-lg"
        @click="$router.push('/login')"
      >
        {{ t('pages.login.title') }}
      </button>
    </div>
  </nav>

  <div class="h-10svh" />
  <div class="flex items-center justify-center">
    <div class="max-w-350 flex flex-col items-center justify-center xl:flex-row-reverse">
      <img
        src="/images/card.png" alt="Fintasy Logo" class="m-15 h-36 md:h-72 sm:h-48"
        style="filter: drop-shadow(8px 24px 24px rgba(5, 150, 105, .8));"
      >
      <div class="m-15">
        <div class="text-4xl text--c-accent lg:text-6xl md:text-5xl">
          Take Your Stocks To The Next Level
        </div>
        <div class="pt-10 text-base md:text-lg">
          Fintasy is a stock market simulator that allows you to trade stocks with fake money. Compete against your
          friends and see who can make the most money!
        </div>
      </div>
    </div>
  </div>
</template>

<route lang="yaml">
  meta:
    layout: default
</route>
