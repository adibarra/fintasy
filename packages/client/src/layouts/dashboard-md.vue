<template>
  <n-layout position="absolute" h-full>
    <NavBar />
    <n-layout has-sider :style="{ height: 'calc(100% - 48px)' }">
      <SideBar />
      <n-layout-content h-full w-full bg--c-bg>
        <div h-fit w-full flex flex-col px-6 py-4 text--c-text>
          <div mx-auto w-fit bg--c-fg px-16 py-4>
            <RouterView />
          </div>
        </div>
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>
