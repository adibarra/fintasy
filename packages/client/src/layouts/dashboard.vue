<template>
  <n-layout position="absolute" h-full>
    <NavBar />
    <n-layout has-sider :style="{ height: 'calc(100% - 48px)' }">
      <SideBar />
      <n-layout-content h-full w-full bg--c-bg-primary>
        <div h-full w-full flex flex-col px-6 py-4 text--c-text>
          <RouterView />
        </div>
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>
