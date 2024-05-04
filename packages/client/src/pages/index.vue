<!--
  @author: Mariptime (Akshay)
  @description: This component is used to display the home page of the application.
-->

<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.main.title')} • Fintasy`,
})
</script>

<template>
  <div h-10svh />
  <div flex items-center justify-center>
    <div max-w-350 flex flex-col items-center justify-center xl:flex-row-reverse>
      <img
        src="/images/card.png"
        alt="Fintasy Logo"
        m-15 h-36 md:h-72 sm:h-48
        style="filter: drop-shadow(8px 24px 24px rgba(5, 150, 105, .8));"
      >
      <div m-15>
        <div text-4xl text--c-accent lg:text-6xl md:text-5xl>
          {{ t('pages.main.content-title') }}
        </div>
        <div pt-10 text-base md:text-lg>
          {{ t('pages.main.content-subtitle') }}
        </div>
      </div>
    </div>
  </div>
  <div grow />
  <span op-10>{{ (import.meta.env.COMMIT_SHA ?? '').slice(0, 7) }}</span>
</template>

<route lang="yaml">
  meta:
    layout: home
</route>
