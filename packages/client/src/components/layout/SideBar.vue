<script setup lang="ts">
import { type MenuOption, NIcon } from 'naive-ui'
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
const store = useSidebarStore()
const menuOptions1: MenuOption[] = [
  { label: `${t('pages.dashboard.title')}`, key: '/dashboard', icon: renderIcon(DashboardIcon) },
  { label: `${t('pages.trade.title')}`, key: '/dashboard/trade', icon: renderIcon(TradeIcon) },
  { label: `${t('pages.tournaments.title')}`, key: '/dashboard/tournaments', icon: renderIcon(TournamentIcon) },
]

const menuOptions2: MenuOption[] = [
  { key: 'divider-1', type: 'divider' },
  { label: `${t('pages.help.title')}`, key: '/dashboard/help', icon: renderIcon(HelpIcon) },
  { label: `${t('pages.settings.title')}`, key: '/dashboard/settings', icon: renderIcon(SettingsIcon) },
]

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) })
}
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
            :options="menuOptions1"
            :root-indent="18"
            @update:value="(key: string) => {
              $router.push(key)
            }"
          />
        </n-scrollbar>
      </div>
      <n-menu
        :options="menuOptions2"
        @update:value="(key: string) => {
          $router.push(key)
        }"
      />
    </div>
  </n-layout-sider>
</template>
