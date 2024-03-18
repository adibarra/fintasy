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
  <n-layout-header bordered h-48px w-full flex>
    <div flex grow items-center gap-5 py-1 pr-5>
      <!-- parent should be w-55 to match sidebar size -->
      <div h-full w-55 flex items-center justify-center>
        <Logo />
      </div>

      <!-- refresh button -->
      <n-tooltip>
        <template #trigger>
          <n-button text hidden lg:block @click="$router.go(0)">
            <n-icon size="20">
              <RefreshIcon />
            </n-icon>
          </n-button>
        </template>
        Refresh Page
      </n-tooltip>

      <!-- breadcrumbs keep track of what page you are on -->
      <n-breadcrumb hidden lg:block>
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

      <!-- coins -->
      <div hidden w-fit items-center justify-center fn-outline px-2 op-85 md:flex>
        Coins: 🪙 {{ user.coins }}
      </div>

      <!-- switch user portfolio trading account -->
      <div hidden w-fit cursor-pointer items-center justify-center fn-outline px-2 op-85 sm:flex fn-hover>
        <n-dropdown
          :options="user.accounts"
          trigger="hover"
          @select="(key, option) => {
            user.account = user.accounts[key].label
            message.info(`Selected ${option.label}`)
          }"
        >
          <div gap-1>
            {{ user.account }}
            <n-icon size="10">
              <DropdownIcon />
            </n-icon>
          </div>
        </n-dropdown>
      </div>

      <!-- theme switch -->
      <ThemeSwitch />

      <!-- notifications with badge -->
      <n-tooltip>
        <template #trigger>
          <n-button text @click="() => message.info(`Clicked notifications`)">
            <n-badge dot processing>
              <n-icon size="22">
                <BellIcon />
              </n-icon>
            </n-badge>
          </n-button>
        </template>
        Notifications
      </n-tooltip>

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
        />
      </n-dropdown>
    </div>
  </n-layout-header>
</template>
