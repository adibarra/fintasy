<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to provide the global theme and configuration for the application.
-->

<script setup lang="ts">
import { darkTheme } from 'naive-ui'

const theme = computed(() => (colorTheme.value === 'dark' ? darkTheme : null))
</script>

<template>
  <n-config-provider :theme="theme">
    <n-global-style />
    <n-loading-bar-provider>
      <n-message-provider>
        <n-notification-provider>
          <n-dialog-provider>
            <slot />
          </n-dialog-provider>
        </n-notification-provider>
      </n-message-provider>
    </n-loading-bar-provider>
  </n-config-provider>
</template>
