<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the dashboard layout of the application.
-->

<script setup lang="ts">
const { width } = useWindowSize()
const isMobile = computed(() => width.value <= 640)
</script>

<template>
  <n-layout position="absolute" h-full>
    <NavBar />
    <n-layout has-sider :style="{ height: isMobile ? 'calc(100% - 108px)' : 'calc(100% - 48px)' }">
      <SideBar v-if="!isMobile" />
      <n-layout-content bg--c-bg text--c-text>
        <div min-h-full w-full flex>
          <div w-full flex grow flex-col px-6 py-4>
            <RouterView />
          </div>
        </div>
      </n-layout-content>
    </n-layout>
    <FooterBar v-if="isMobile" />
  </n-layout>
</template>
