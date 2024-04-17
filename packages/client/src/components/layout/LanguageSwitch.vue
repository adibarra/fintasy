<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to switch the language of the application.
-->

<script setup lang="ts">
import {
  Language as LanguageIcon,
} from '@vicons/carbon'
import { useMessage } from 'naive-ui'
import { availableLocales, loadLanguageAsync } from '~/modules/i18n'

const { t, locale } = useI18n()
const message = useMessage()

async function setLocale(newLocale: string) {
  await loadLanguageAsync(newLocale)
  locale.value = newLocale
  message.info(`${t('i18n.language-changed-to')} ${newLocale}`)
}

const locales = computed(() => {
  const locales = [
    { key: 0, label: t('i18n.change-language'), type: 'header', disabled: true },
    { key: 1, type: 'divider' },
    ...availableLocales.map(locale => ({ key: `locale-${locale}`, label: locale })),
  ]
  return locales
})
</script>

<template>
  <n-dropdown
    :options="locales"
    @select="(_, option) => setLocale(option.label as string)"
  >
    <n-button text>
      <n-icon size="22">
        <LanguageIcon />
      </n-icon>
    </n-button>
  </n-dropdown>
</template>
