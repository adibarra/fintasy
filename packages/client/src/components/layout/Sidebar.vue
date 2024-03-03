<script setup lang="ts">
import { type MenuOption, NIcon } from 'naive-ui'
import {
  Home as HomeIcon,
  Settings as SettingsIcon,
} from '@vicons/carbon'
import { useSidebarStore } from '~/stores/sidebar'

const store = useSidebarStore()
const menuOptions: MenuOption[] = [
  { label: 'Home', key: '/', icon: renderIcon(HomeIcon) },
  { key: 'divider-1', type: 'divider' },
  { label: 'Settings', key: '/settings', icon: renderIcon(SettingsIcon) },
]

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) })
}
</script>

<template>
  <n-layout-sider
    :width="220"
    :native-scrollbar="false"
    :collapsed="store.collapsed"
    collapse-mode="width"
    show-trigger="bar"
    bordered
    @update:collapsed="store.toggle"
  >
    <n-menu
      :options="menuOptions"
      @update:value="(key: string, item: MenuOption) => {
        $router.push(key)
      }"
    />
  </n-layout-sider>
</template>
