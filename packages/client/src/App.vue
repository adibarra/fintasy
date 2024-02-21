<script setup lang="ts">
useHead({
  title: 'Fintasy',
  meta: [
    {
      name: 'description',
      content: 'A competitive paper trading platform',
    },
  ],
  link: [
    {
      rel: 'icon',
      type: 'image/svg+xml',
      href: () => preferredDark.value ? '/favicon-dark.svg' : '/favicon.svg',
    },
  ],
})
</script>

<template>
  <div flex flex-col min-h-svh text--c-text>
    <RouterView />
  </div>
</template>
