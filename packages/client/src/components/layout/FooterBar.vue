<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the footer bar at the bottom of the application.
-->

<script setup lang="ts">
import { NIcon } from 'naive-ui'
import type { MenuInst, MenuOption } from 'naive-ui'
import {
  Dashboard as DashboardIcon,
  Help as HelpIcon,
  Settings as SettingsIcon,
  ArrowsHorizontal as TradeIcon,
} from '@vicons/carbon'
import {
  Tournament as TournamentIcon,
} from '@vicons/tabler'

const { t } = useI18n()
const route = useRoute()
const menuOptions1: MenuOption[] = [
  { key: '/dashboard', icon: renderIcon(DashboardIcon) },
  { key: '/dashboard/trade', icon: renderIcon(TradeIcon) },
  { key: '/dashboard/tournaments', icon: renderIcon(TournamentIcon) },
]

const menuOptions2: MenuOption[] = [
  { key: '/dashboard/help', icon: renderIcon(HelpIcon), children: [
    { label: `${t('pages.dashboard.help.index.title')}`, key: '/dashboard/help' },
    { label: `${t('pages.dashboard.help.faq.title')}`, key: '/dashboard/help/faq' },
  ] },
  { key: '/dashboard/settings', icon: renderIcon(SettingsIcon) },
]

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const menu1SelectedKey = ref('')
const menu2SelectedKey = ref('')
const menu1 = ref<MenuInst | null>(null)
const menu2 = ref<MenuInst | null>(null)
function selectAndExpand(key: string) {
  menu1SelectedKey.value = key
  menu2SelectedKey.value = key
  menu1.value?.showOption(key)
  menu2.value?.showOption(key)
}

watch(() => route.path, () => {
  selectAndExpand(route.path)
}, { immediate: true })
</script>

<template>
  <n-layout-footer bordered h-42px>
    <div flex>
      <n-scrollbar>
        <n-menu
          ref="menu1"
          v-model:value="menu1SelectedKey"
          :options="menuOptions1"
          mode="horizontal"
          collapsed responsive
          @update:value="(key: string) => {
            $router.push(key)
          }"
        />
      </n-scrollbar>
      <div w-fit>
        <n-menu
          ref="menu2"
          v-model:value="menu2SelectedKey"
          :options="menuOptions2"
          mode="horizontal"
          collapsed responsive
          @update:value="(key: string) => {
            $router.push(key)
          }"
        />
      </div>
    </div>
  </n-layout-footer>
</template>
