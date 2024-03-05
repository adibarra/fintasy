<script setup lang="ts">
import {
  NotificationsOutline as BellIcon,
  CaretDownOutline as DropdownIcon,
  RefreshOutline as RefreshIcon,
} from '@vicons/ionicons5'
import { useMessage } from 'naive-ui'

const { t } = useI18n()
const route = useRoute()
const message = useMessage()

interface Crumb { label: string, key: string }
const breadcrumbs = computed(() => {
  const parts = route.path.split('/').filter(Boolean)

  let path = ''
  const crumbs: Crumb[] = parts.map((part: string) => {
    path += `/${part}`
    return {
      label: t(`pages.${path.replaceAll('/', '.').slice(1)}.title`),
      key: path,
    }
  })

  if (crumbs.length === 1)
    crumbs.push({ label: t('misc.home'), key: crumbs[0].key })

  return crumbs
})

const user = ref({
  name: 'adibarra',
  avatar: 'https://avatars.githubusercontent.com/u/93070681?v=4',
  account: 'Trading Account 1',
  accounts: [
    { label: 'Trading Account 1', key: 0 },
    { label: 'Trading Account 2', key: 1 },
    { label: 'Trading Account 3', key: 2 },
  ],
  coins: 50,
  balance: 200,
})
</script>

<template>
  <n-layout-header bordered h-48px flex items-center py-1>
    <!-- parent should be w-55 to match sidebar size -->
    <div mr-5 h-full w-55 flex items-center justify-center px-2>
      <Logo />
    </div>

    <!-- refresh button -->
    <n-tooltip>
      <template #trigger>
        <n-button text mr-5 @click="$router.go(0)">
          <n-icon size="20" :depth="2">
            <RefreshIcon />
          </n-icon>
        </n-button>
      </template>
      Refresh Page
    </n-tooltip>

    <!-- breadcrumbs keep track of what page you are on -->
    <n-breadcrumb mr-5>
      <template v-for="crumb in breadcrumbs" :key="crumb">
        <n-breadcrumb-item>
          <router-link :to="crumb.key">
            {{ crumb.label }}
          </router-link>
        </n-breadcrumb-item>
      </template>
    </n-breadcrumb>

    <!-- spacer to push the rest of the items to the right -->
    <div grow />

    <!-- just a bunch of placeholders from here on -->
    <!-- need to work on look and feel as well as the actual logic for them -->

    <!-- coins -->
    <div ml-5 w-fit flex items-center justify-center bg--c-bg-tertiary px-2 op-85>
      Coins: 🪙 {{ user.coins }}
    </div>

    <!-- balance -->
    <div ml-5 w-fit flex items-center justify-center bg--c-bg-tertiary px-2 op-85>
      Balance: ${{ user.balance }}
    </div>

    <!-- switch user portfolio trading account -->
    <n-dropdown
      :options="user.accounts"
      trigger="hover"
      @select="(key, option) => {
        user.account = user.accounts[key].label
        message.info(`Selected ${option.label}`)
      }"
    >
      <div ml-5 w-fit flex items-center justify-center gap-1 bg--c-bg-tertiary px-2 op-85>
        {{ user.account }}
        <n-icon :depth="2" size="10">
          <DropdownIcon />
        </n-icon>
      </div>
    </n-dropdown>

    <!-- notifications with badge -->
    <n-badge dot processing>
      <n-icon
        :depth="2" size="22" ml-5
        @click="() => message.info(`Clicked notifications`)"
      >
        <BellIcon />
      </n-icon>
    </n-badge>

    <!-- user dropdown -->
    <n-dropdown
      :options="[
        { label: 'Profile', key: 'profile' },
        { label: 'Settings', key: 'settings' },
        { label: 'Logout', key: 'logout' },
      ]"
      trigger="hover"
      @select="(key) => message.info(`Selected ${key}`)"
    >
      <n-avatar
        size="small"
        :src="user.avatar"
        mx-5
      />
    </n-dropdown>
  </n-layout-header>
</template>
