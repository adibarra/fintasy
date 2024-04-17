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
    layout: home
</route>
