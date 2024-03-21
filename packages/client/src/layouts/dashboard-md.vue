<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the dashboard layout of the application with markdown rendered content.
-->

<script setup lang="ts">
const { width } = useWindowSize()
const isMobile = computed(() => width.value <= 640)
</script>

<template>
  <n-layout position="absolute" h-full>
    <NavBar />
    <n-layout has-sider :style="{ height: isMobile ? 'calc(100% - 90px)' : 'calc(100% - 48px)' }">
      <SideBar v-if="!isMobile" />
      <n-layout-content class="dots" bg--c-bg text--c-text>
        <div min-h-full w-full px-6 py-4>
          <div mx-auto max-w-full w-fit bg--c-fg px-16 py-4>
            <RouterView />
          </div>
        </div>
      </n-layout-content>
    </n-layout>
    <FooterBar v-if="isMobile" />
  </n-layout>
</template>

<style scoped>
.dots {
  background-image: radial-gradient(hsla(0, 0%, 100%, 0.1) 1px, transparent 0);
  background-size: 2rem 2rem;
}
</style>
