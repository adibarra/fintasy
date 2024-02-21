<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.main.title')} • Fintasy`,
})
</script>

<template>
  <main flex flex-col grow px-4>
    <div flex flex-col w-92vw max-w-400 mx-auto my-auto grow>
      {{ $t('example.hello-world') }}
    </div>
  </main>
</template>
