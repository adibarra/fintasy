<script setup lang="ts">
useHead({
  title: 'Fintasy',
  meta: [
    {
      name: 'description',
      content: 'A competitive paper trading platform',
    },
  ],
  link: [
    {
      rel: 'icon',
      type: 'image/svg+xml',
      href: () => preferredDark.value ? '/favicon-dark.svg' : '/favicon.svg',
    },
  ],
})
</script>

<template>
  <Provider>
    <RouterView />
  </Provider>
</template>

<style>
:root {
  color-scheme: light dark;
  --c-bg-primary: #ededed;
  --c-bg-secondary: #e2e2e2;
  --c-bg-tertiary: #dbdbdb;
  --c-fg-primary: #d3d3d3;
  --c-fg-secondary: #cdcdcd;
  --c-fg-tertiary: #c8c8c8;
  --c-text: #151515;
  --c-inverse: #121212;
  --c-accent: #1da54f;
}

html.dark {
  --c-bg-primary: #121212;
  --c-bg-secondary: #1d1d1d;
  --c-bg-tertiary: #242424;
  --c-fg-primary: #2c2c2c;
  --c-fg-secondary: #323232;
  --c-fg-tertiary: #373737;
  --c-text: #eaeaea;
  --c-inverse: #ededed;
  --c-accent: #4ade80;
}

html,
body,
#app {
  height: 100%;
  margin: 0;
  padding: 0;
  background: transparent;
  background: var(--c-bg-primary);
}

html,
div {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

html::-webkit-scrollbar,
div::-webkit-scrollbar {
  display: none;
}

#nprogress {
  pointer-events: none;
}

#nprogress .bar {
  background: var(--c-accent);
  opacity: 0.75;
  position: fixed;
  z-index: 1031;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
}
</style>
