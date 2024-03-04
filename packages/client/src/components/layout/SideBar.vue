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
import { useSidebarStore } from '~/stores/sidebar'

const { t } = useI18n()
const route = useRoute()
const store = useSidebarStore()
const menuOptions1: MenuOption[] = [
  { label: `${t('pages.dashboard.title')}`, key: '/dashboard', icon: renderIcon(DashboardIcon) },
  { label: `${t('pages.dashboard.trade.title')}`, key: '/dashboard/trade', icon: renderIcon(TradeIcon) },
  { label: `${t('pages.dashboard.tournaments.title')}`, key: '/dashboard/tournaments', icon: renderIcon(TournamentIcon) },
]

const menuOptions2: MenuOption[] = [
  { key: 'divider-1', type: 'divider' },
  { label: `${t('pages.dashboard.help.title')}`, key: '/dashboard/help', icon: renderIcon(HelpIcon), children: [
    { label: `${t('pages.dashboard.help.index.title')}`, key: '/dashboard/help', icon: renderIcon(HelpIcon) },
    { label: `${t('pages.dashboard.help.faq.title')}`, key: '/dashboard/help/faq', icon: renderIcon(HelpIcon) },
  ] },
  { label: `${t('pages.dashboard.settings.title')}`, key: '/dashboard/settings', icon: renderIcon(SettingsIcon) },
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
})
</script>

<template>
  <n-layout-sider
    :width="220"
    :collapsed="store.collapsed"
    collapse-mode="width"
    show-trigger="bar"
    bordered
    @update:collapsed="store.toggle"
  >
    <div h-full flex flex-col>
      <div min-h-0 flex-1>
        <n-scrollbar>
          <n-menu
            ref="menu1"
            v-model:value="menu1SelectedKey"
            :options="menuOptions1"
            @update:value="(key: string) => {
              $router.push(key)
            }"
          />
        </n-scrollbar>
      </div>
      <n-menu
        ref="menu2"
        v-model:value="menu2SelectedKey"
        :options="menuOptions2"
        @update:value="(key: string) => {
          $router.push(key)
        }"
      />
    </div>
  </n-layout-sider>
</template>
