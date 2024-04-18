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
    <router-link
      to="/"
      focusable="false"
      absolute m-2 flex select-none gap-3 outline-none lg:fixed
    >
      <img src="/pwa-512x512.png" alt="Fintasy Logo" mr-2 h-15>
      <div my-auto text-3xl>
        Fintasy
      </div>
    </router-link>

    <nav flex flex-row items-center gap-5 p-2>
      <!-- spacer -->
      <div grow />

      <!-- home link -->
      <n-tooltip>
        <template #trigger>
          <n-button text @click="$router.push('/')">
            <span lt-md:hidden>{{ t('misc.home') }}</span>
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
            <span lt-md:hidden>{{ t('pages.dashboard.title') }}</span>
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
