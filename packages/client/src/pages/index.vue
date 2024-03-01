<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.main.title')} • Fintasy`,
})
</script>

<template>
  <main flex grow flex-col px-4>
    <div mx-auto my-auto max-w-400 w-92vw flex grow flex-col>
      {{ $t('example.hello-world') }}
    </div>
  </main>
</template>
