<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the dashboard layout of the application.
-->

<template>
  <n-layout position="absolute" h-full>
    <NavBar />
    <n-layout has-sider :style="{ height: 'calc(100% - 48px)' }">
      <SideBar />
      <n-layout-content h-full w-full bg--c-bg>
        <div h-full w-full flex>
          <div flex grow flex-col px-6 py-4 text--c-text>
            <RouterView />
          </div>
        </div>
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>
