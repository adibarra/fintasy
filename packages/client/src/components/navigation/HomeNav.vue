<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the home navigation bar.
-->

<script setup lang="ts">
import {
  HomeOutline as HomeIcon,
} from '@vicons/ionicons5'
import {
  Dashboard as DashboardIcon,
} from '@vicons/carbon'

const { t } = useI18n()
</script>

<template>
  <header z-40 text-lg>
    <nav flex flex-row items-center gap-5 p-2>
      <!-- logo -->
      <router-link
        to="/"
        focusable="false"
        flex select-none gap-3 outline-none
      >
        <img src="/pwa-512x512.png" alt="Fintasy Logo" mr-2 h-8 md:h-12>
        <div my-auto md:text-3xl>
          Fintasy
        </div>
      </router-link>

      <!-- spacer -->
      <div grow />

      <!-- home link -->
      <n-tooltip>
        <template #trigger>
          <n-button text @click="$router.push('/')">
            <span lt-md:hidden md:text-lg>
              {{ t('misc.home') }}
            </span>
            <n-icon size="22" md:hidden>
              <HomeIcon />
            </n-icon>
          </n-button>
        </template>
        {{ t('misc.home') }}
      </n-tooltip>

      <!-- dashboard link -->
      <n-tooltip>
        <template #trigger>
          <n-button text @click="$router.push('/dashboard')">
            <span lt-md:hidden md:text-lg>
              {{ t('pages.dashboard.title') }}
            </span>
            <n-icon size="22" md:hidden>
              <DashboardIcon />
            </n-icon>
          </n-button>
        </template>
        {{ t('pages.dashboard.title') }}
      </n-tooltip>

      <LanguageSwitch />
      <ThemeSwitch />
    </nav>
  </header>
</template>
