<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.main.title')} • Fintasy`,
})
</script>

<template>
  <nav class="mx-10 my-4 flex justify-between lg:flex-row md:flex-row xl:flex-row sm:flex-col">
    <router-link to="/" class="flex items-center justify-center">
      <img
        src="/pwa-192x192.png" alt="Fintasy Logo"
        class="mr-2 h-14 lg:mb-2 lg:mr-0 md:mb-2 md:mr-0 sm:mb-4 xl:mb-2 xl:mr-0"
      >

      <div class="pl-2 text-4xl lg:text-4xl md:text-3xl sm:text-2xl xl:text-4xl">
        Fintasy
      </div>
    </router-link>
    <div class="flex items-center">
      <button
        class="ml-10 rd-10 px-4 py-2 text-lg hover:text--c-accent"
        @click="$router.push('/dashboard')"
      >
        {{ t('pages.dashboard.title') }}
      </button>

      <button
        class="ml-10 rd-10 bg--c-inverse hover:bg--c-accent px-4 py-2 text-lg text--c-bg"
        @click="$router.push('/login')"
      >
        {{ t('pages.login.title') }}
      </button>
    </div>
  </nav>

  <div class="my-25 flex flex-col-reverse items-center justify-center lg:flex-row md:flex-row sm:flex-row xl:flex-row">
    <div class="mx-5 my-15 lg:mx-55 md:mx-15 sm:mx-10 xl:mx-55">
      <div class="text-8xl text--c-accent -mr-50 lg:text-6xl md:text-5xl sm:text-4xl xl:text-8xl">
        Take Your Stocks To The Next Level
      </div>
      <div class="py-10 text-lg lg:text-lg md:text-lg sm:text-base xl:text-lg">
        Fintasy is a stock market simulator that allows you to trade stocks with fake money. Compete against your
        friends and see who can make the most money!
      </div>
    </div>

    <img
      src="/images/card.png" alt="Fintasy Logo" class="mr-5 h-96 lg:mr-55 md:mr-15 sm:mr-10 xl:mr-55"
      style="filter: drop-shadow(8px 24px 24px rgba(5, 150, 105, .8));"
    >
  </div>

  <!-- Some spacers and a temporary footer -->
  <span class="opacity-50">
    <div class="h-10" />
    [ pages/index.vue ]
    <div class="h-10" />
  </span>
</template>

<route lang="yaml">
  meta:
    layout: default
</route>

<style scoped>
@media screen and (max-width: 640px) {
  /* Small devices (phones) */
  .flex-col-reverse {
    flex-direction: column-reverse;
  }
}
</style>
