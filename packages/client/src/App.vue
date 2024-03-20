<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is the root of the application.
-->

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
  --c-bg: #ededed;
  --c-fg: #ffffff;
  --c-text: #151515;
  --c-inverse: #121212;
  --c-accent: #1da54f;
}

html.dark {
  --c-bg: #121212;
  --c-fg: #1b1b1b;
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
  background: var(--c-bg);
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

.prose pre:not(.shiki) {
  padding: 0;
}

.prose .shiki {
  font-family: 'DM Mono', monospace;
  font-size: 1.2em;
  line-height: 1.4;
  background: var(--c-bg);
}

.prose img {
  width: 100%;
}

.shiki,
.shiki span {
  color: var(--shiki-light);
}

html.dark .shiki,
html.dark .shiki span {
  color: var(--shiki-dark);
}
</style>
