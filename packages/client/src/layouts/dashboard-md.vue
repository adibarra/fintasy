<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the dashboard layout of the application with markdown rendered content.
-->

<template>
  <n-layout position="absolute" h-full>
    <NavBar />
    <n-layout has-sider :style="{ height: 'calc(100% - 48px)' }">
      <SideBar />
      <n-layout-content class="dots" h-full w-full bg--c-bg>
        <div h-fit w-full px-6 py-4 text--c-text>
          <div mx-auto w-fit bg--c-fg px-16 py-4>
            <RouterView />
          </div>
        </div>
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

<style scoped>
.dots {
  background-image: radial-gradient(hsla(0, 0%, 100%, 0.1) 1px, transparent 0);
  background-size: 2rem 2rem;
}
</style>
