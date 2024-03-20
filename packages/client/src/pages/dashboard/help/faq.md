<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display a FAQ page for the application.
-->

# Another Example

This is another example of a markdown file. This time, it is a FAQ page placeholder.

Additionally, you can see that there is a mysterious vue component called `I18nTitle`. It is used to set the page's title so that it is translated and displayed correctly in the browser's title bar. Every markdown page should have one of these.

There is nothing else to see here.
<router-link to="/dashboard/help">Go Back</router-link>

<!-- Some spacers and a temporary footer -->
<span op-50>
  <div h-20 />
  [ pages/dashboard/help/faq.md ]
  <div h-10 />
</span>

<I18nTitle title="pages.dashboard.help.faq.title" />

<route lang="yaml">
  meta:
    layout: dashboard-md
</route>
