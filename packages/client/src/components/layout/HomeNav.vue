<script setup lang="ts">
const { t } = useI18n()
const route = useRoute()

const buttonName = computed(() => {
  if (route.path === '/')
    return t('pages.login.title')

  return t('misc.home')
})
const buttonRoute = computed(() => {
  if (route.path === '/')
    return '/login'

  return '/'
})
</script>

<template>
  <nav mb-8 flex md:mx-6 md:my-4>
    <router-link to="/" flex items-center justify-center gap-2>
      <img src="/pwa-192x192.png" alt="Fintasy Logo" h-14>
      <div text-2xl lg:text-4xl md:text-3xl>
        Fintasy
      </div>
    </router-link>
    <div grow />
    <div flex items-center gap-5>
      <button
        rd-10 bg--c-inverse hover:bg--c-accent px-6 py-2 text--c-bg md:text-lg
        @click="$router.push(buttonRoute)"
      >
        {{ buttonName }}
      </button>
    </div>
  </nav>
</template>
