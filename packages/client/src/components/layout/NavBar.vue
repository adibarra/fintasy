<script setup lang="ts">
import { Notification as BellIcon } from '@vicons/carbon'

const { t } = useI18n()
const route = useRoute()

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
  notifications: '99+',
})
</script>

<template>
  <n-layout-header bordered h-45px flex items-center px-2 py-1>
    <!-- logo should be w-51 to be same size as sidebar items -->
    <div mr-5 h-full w-51 flex items-center justify-center bg--c-bg-tertiary>
      <Logo />
    </div>

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
    <div ml-8 w-fit flex items-center justify-center bg--c-bg-tertiary px-2>
      Coins: 🪙 {{ user.coins }}
    </div>

    <!-- balance -->
    <div ml-8 w-fit flex items-center justify-center bg--c-bg-tertiary px-2>
      Balance: ${{ user.balance }}
    </div>

    <!-- switch user portfolio trading account -->
    <n-dropdown
      :options="user.accounts"
      trigger="hover"
      @select="(key) => user.account = user.accounts[key].label"
    >
      <div ml-8 w-fit flex items-center justify-center bg--c-bg-tertiary px-2>
        {{ user.account }}
      </div>
    </n-dropdown>

    <!-- notifications with badge -->
    <n-badge
      :value="user.notifications"
      ml-8
    >
      <n-avatar
        size="small"
        color="transparent"
        cursor-pointer
      >
        <n-icon>
          <BellIcon />
        </n-icon>
      </n-avatar>
    </n-badge>

    <!-- user dropdown -->
    <n-dropdown
      :options="[
        { label: 'Profile', key: 'profile' },
        { label: 'Settings', key: 'settings' },
        { label: 'Logout', key: 'logout' },

      ]"
      trigger="hover"
    >
      <n-avatar
        size="small"
        :src="user.avatar"
        ml-8 mr-5
      />
    </n-dropdown>
  </n-layout-header>
</template>
