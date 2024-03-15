<script setup lang="ts">
import {
  Moon as DarkIcon,
  Sun as LightIcon,
} from '@vicons/carbon'
</script>

<template>
  <n-tooltip>
    <template #trigger>
      <n-button text @click="toggleTheme()">
        <n-icon size="20" :depth="2">
          <DarkIcon v-if="isDark" />
          <LightIcon v-else />
        </n-icon>
      </n-button>
    </template>
    Toggle Theme
  </n-tooltip>
</template>
