<template>
  <n-layout position="absolute" h-full>
    <NavBar />
    <n-layout has-sider :style="{ height: 'calc(100% - 48px)' }">
      <SideBar />
      <n-layout-content>
        <div h-full flex grow flex-col bg--c-bg-primary text--c-text>
          <n-scrollbar p-4>
            <RouterView />
          </n-scrollbar>
        </div>
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>
