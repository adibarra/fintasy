<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to switch the theme of the application.
-->

<script setup lang="ts">
import {
  Moon as DarkIcon,
  Sun as LightIcon,
} from '@vicons/carbon'
import { useMessage } from 'naive-ui'

const { t } = useI18n()
const message = useMessage()
</script>

<template>
  <n-tooltip>
    <template #trigger>
      <n-button
        text @click="() => {
          message.info(t('theme-switch.theme-toggled'))
          toggleTheme()
        }"
      >
        <n-icon size="22">
          <DarkIcon v-if="isDark" />
          <LightIcon v-else />
        </n-icon>
      </n-button>
    </template>
    {{ t('theme-switch.toggle-theme') }}
  </n-tooltip>
</template>
