<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the navigation bar at the top of the application.
-->

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
const state = useStateStore()

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

const portfolios = computed(() => {
  return state.portfolio.available.map((p, i) => ({ key: i, label: p.name }))
})
</script>

<template>
  <n-layout-header bordered h-48px w-full flex>
    <div flex grow items-center gap-5 py-1>
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
        Coins: 🪙 {{ state.user.coins }}
      </div>

      <!-- switch user portfolio account -->
      <div hidden w-fit cursor-pointer items-center justify-center fn-outline px-2 op-85 sm:flex fn-hover>
        <n-dropdown
          :options="portfolios"
          trigger="click"
          @select="(key, option) => {
            state.portfolio.active = key
            message.info(`Selected ${option.label}`)
          }"
        >
          <div gap-1>
            {{ portfolios.length > 0 ? portfolios[state.portfolio.active].label : 'None' }}
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
          { label: 'Logout', key: 'logout' },
        ]"
        trigger="click"
        @select="(key) => message.info(`Selected ${key}`)"
      >
        <n-avatar
          size="small"
          :src="state.user.avatar"
          mr-5 cursor-pointer
        />
      </n-dropdown>
    </div>
  </n-layout-header>
</template>
