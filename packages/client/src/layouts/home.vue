<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the home layout of the application.
-->

<template>
  <div relative flex grow flex-col bg--c-bg p-4 text--c-text min-h-svh>
    <HomeNav />
    <RouterView />
  </div>
</template>
