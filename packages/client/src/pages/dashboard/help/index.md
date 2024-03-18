# Help page

## Introduction

Later on, this page will contain helpful information about how to use the dashboard and the app in general.
We can also add some sections on the basics of the stock market.

## Some text here

This is an example of a page that uses the dashboard layout and is also markdown based.

- We are able to use full markdown syntax here.
- We can also use custom vue components like the `router-link` component to add inter-app links to this page.
  - <router-link to="/dashboard">Go to dashboard</router-link>.

1. External links are also supported.
2. Click [here](https://www.google.com) to go to Google.

## Images

Images are also supported and they can even have captions and css if you do it like this:

<figure>
  <img src="/favicon.svg" alt="Site favicon" rounded-lg h-40 bg--c-bg p-2>
  <figcaption text-right mt-2 op-75>
    This is the website's current favicon.
  </figcaption>
</figure>

You can also have it change depending on the theme.
If you switch between light and dark mode, the image's background will change to match the theme.

## Code blocks

Here is a code block with syntax highlighting:

```js
// This is a comment
console.log('Hello World')
```

However, is recommended to write any necessary html in a vue component in the `/components` folder and import it here instead of writing it directly in the markdown file.

<!-- Some spacers and a temporary footer -->
<span op-50>
  <div h-20 />
  [ pages/dashboard/help/index.md ]
  <div h-10 />
</span>

<I18nTitle title="pages.dashboard.help.title" />

<route lang="yaml">
  meta:
    layout: dashboard-md
</route>
