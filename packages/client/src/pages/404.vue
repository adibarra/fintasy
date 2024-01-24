<script setup lang="ts">
useHead({
  title: 'Not Found',
  meta: [
    { name: 'robots', content: 'noindex, nofollow' },
  ],
})
</script>

<template>
  <main grow>
    <div w-fit p-5 mx-auto mt-20vh outline outline-1 rd-2>
      <div font-900 text-4xl>
        <span text-red>404:</span>
        Not Found
      </div>
      <button
        title="Go Back"
        custom-icon-btn flex text-lg mt-2
        @click="$router.back()"
        @keydown.enter="$router.back()"
      >
        <div i-carbon:caret-left text-2xl />
        Go Back
      </button>
    </div>
  </main>
</template>

<route lang="yaml">
meta:
  layout: default
</route>
