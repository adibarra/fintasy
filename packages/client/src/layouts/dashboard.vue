<template>
  <n-layout position="absolute" h-full>
    <NavBar />
    <n-layout has-sider :style="{ height: 'calc(100% - 45px)' }">
      <SideBar />
      <n-layout-content>
        <RouterView />
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>
