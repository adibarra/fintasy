<!--
  @author: Mariptime (Akshay)
  @description: This component is used to display the login/register page of the application.
-->

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

useHead({
  title: `${t('pages.login.title')} • Fintasy`,
})

const email = ref('')
const password = ref('')

function submitForm() {
  // Implement your form submission logic here
}

function authenticateWithGoogle() {
  // Implement Google authentication logic
}

function authenticateWithFacebook() {
  // Implement Facebook authentication logic
}
</script>

<template>
  <nav class="flex md:mx-6 md:my-4">
    <router-link to="/" class="flex items-center justify-center gap-2">
      <img src="/pwa-192x192.png" alt="Fintasy Logo" class="h-14">
      <div class="text-2xl lg:text-4xl md:text-3xl">
        Fintasy
      </div>
    </router-link>
    <div class="grow" />
    <div class="flex items-center gap-5">
      <button class="rd-10 bg--c-accent hover:bg--c-inverse px-6 py-2 text--c-bg md:text-lg" @click="$router.push('/')">
        {{ t('Home') }}
      </button>
    </div>
  </nav>
  <div style="filter: drop-shadow(0px 0px 12px rgba(5, 150, 105, 2));" class="bg-white px-10 py-8 md:mx-96 md:my-24">
    <div class="mb-4 flex justify-center gap-2">
      <router-link to="/login" class="flex items-center justify-center gap-2">
        <button class="bg-emerald-600 px-4 py-2 text-white">
          {{ t('Login') }}
        </button>
      </router-link>
      <router-link to="/register" class="flex items-center justify-center gap-2">
        <button class="bg-emerald-600 px-4 py-2 text-white">
          {{ t('Register') }}
        </button>
      </router-link>
    </div>

    <div>
      <!-- Login form -->
      <form class="space-y-4" @submit.prevent="submitForm">
        <div class="text-4xl text-emerald-600 lg:text-2xl md:text-5xl">
          <label for="email" class="block">{{ t('Enter your Email') }}</label>
          <input
            id="email" v-model="email" type="text" required
            class="mt-1 w-full border bg-white p-2 text-black"
          >
        </div>

        <div class="text-4xl text-emerald-600 lg:text-2xl md:text-5xl">
          <label for="Enter your Password" class="block">{{ t('Enter your Password') }}</label>
          <input
            id="password" v-model="password" type="password" required
            class="mt-1 w-full border bg-white p-2 text-black"
          >
        </div>

        <button type="submit" class="w-full bg-emerald-600 p-2 text-white" @click="$router.push('/dashboard')">
          {{ t('Login') }}
        </button>

        <div class="mt-10">
          <p class="mb-2 text-black">
            {{ t('Or Login with Socials') }}:
          </p>
          <div class="flex">
            <button class="mb-2 mr-4 w-full bg-red-500 p-2 text-white" @click="authenticateWithGoogle">
              {{ t('Google') }}
            </button>
            <button class="mb-2 ml-4 w-full bg-blue-500 p-2 text-white" @click="authenticateWithFacebook">
              {{ t('Facebook') }}
            </button>
          </div>
          <!-- Add more buttons for other third-party authentication options as needed -->
        </div>
      </form>
    </div>
  </div>
</template>

<route lang="yaml">
  meta:
    layout: default
</route>
