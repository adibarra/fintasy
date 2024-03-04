# Another Example

This is another example of a markdown file.

There is nothing else to see here
<router-link to="/dashboard/help">Go Back</router-link>

<span op-50>
  <!-- Some spacers and a temporary footer -->
  <div h-10 />
  [ pages/dashboard/help/faq.md ]
  <div h-10 />
</span>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
useHead({
  title: `${t('pages.dashboard.help.faq.title')} • Fintasy`,
})
</script>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
