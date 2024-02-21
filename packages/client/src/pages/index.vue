<script setup lang="ts">
useHead({
  title: 'Fintasy',
})
</script>

<template>
  <main flex flex-col grow px-4>
    <div flex flex-col w-92vw max-w-400 mx-auto my-auto grow>
      {{ t('intro.hello-world') }}
    </div>
  </main>
</template>
