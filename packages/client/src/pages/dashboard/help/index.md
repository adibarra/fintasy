# Help page

## Introduction

Later on, this page will contain helpful information about how to use the dashboard and the app in general.
We can also add some sections on the basics of the stock market.

## Some text here

This is an example of a page that uses the dashboard layout and is also markdown based.

- We are able to use full markdown syntax here.
- We can also use custom components like the `router-link` component to add inter-app links to this page.
  <router-link to="/dashboard">Go to dashboard</router-link> or <router-link to="/dashboard/help/example">Go to another example</router-link>

Click [here](https://www.google.com) to go to Google.

## Code blocks

Here is a code block with syntax highlighting:

```js
// This is a comment
console.log('Hello World')
```

You can also add plain HTML to the markdown file.
This is a simple HTML button:

<button fn-outline fn-outline-hover py-1 px-2 @click="(e) => {
const demo_button = e.target as HTMLButtonElement
let times = Number.parseInt(demo_button.getAttribute('data-clicks') || '0') + 1
demo_button.innerText = Number.isNaN(times) ? 'Clicked!' : `Clicked x${times}`;
demo_button.setAttribute('data-clicks', times.toString());
}">
Click me
</button>

However, is recommended to write any necessary html in a vue component in the `/components` folder and import it here instead of writing it directly in the markdown file.

<span op-50>
  <!-- Some spacers and a temporary footer -->
  <div h-10 />
  [ pages/dashboard/help/index.md ]
  <div h-10 />
</span>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
useHead({
  title: `${t('pages.dashboard.help.title')} • Fintasy`,
})
</script>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
