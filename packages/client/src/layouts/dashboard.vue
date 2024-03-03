<template>
  <n-layout position="absolute" has-sider>
    <sidebar />
    <n-layout>
      <Header />
      <RouterView />
      <Footer />
    </n-layout>
  </n-layout>
</template>
