<script setup lang="ts">
import {
  Moon as DarkIcon,
  Sun as LightIcon,
} from '@vicons/carbon'
import { useMessage } from 'naive-ui'

const message = useMessage()
</script>

<template>
  <n-tooltip>
    <template #trigger>
      <n-button text @click="() => { message.info(`Toggled Theme`); toggleTheme() }">
        <n-icon size="22">
          <DarkIcon v-if="isDark" />
          <LightIcon v-else />
        </n-icon>
      </n-button>
    </template>
    Toggle Theme
  </n-tooltip>
</template>
