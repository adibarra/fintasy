<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the 404 page of the application.
-->

<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('errors.not-found')} • Fintasy`,
  meta: [
    { name: 'robots', content: 'noindex, nofollow' },
  ],
})
</script>

<template>
  <div h-20vh />
  <div mx-auto w-fit rd-2 p-5 outline-1 outline>
    <div text-4xl font-900>
      <span text-red>404:</span>
      {{ $t('errors.not-found') }}
    </div>
    <button
      :title="$t('buttons.go-back')"
      mt-2 flex text-lg fn-icon-btn
      @click="$router.back()"
      @keydown.enter="$router.back()"
    >
      <div i-carbon:caret-left text-2xl />
      {{ $t('buttons.go-back') }}
    </button>
  </div>
  <div grow />
</template>

<route lang="yaml">
  meta:
    layout: default
</route>
