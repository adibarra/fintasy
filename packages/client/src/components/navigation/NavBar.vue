<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the navigation bar at the top of the application.
-->

<script setup lang="ts">
import {
  AddOutline as AddIcon,
  NotificationsOutline as BellIcon,
  CaretDownOutline as DropdownIcon,
  LogOutOutline as LogoutIcon,
  RefreshOutline as RefreshIcon,
  PersonCircleOutline as UserIcon,
} from '@vicons/ionicons5'
import { NIcon, useMessage } from 'naive-ui'
import { createAvatar } from '@dicebear/core'
import { identicon } from '@dicebear/collection'

const { t, locale } = useI18n()
const fintasy = useAPI()
const state = useStateStore()
const message = useMessage()
const route = useRoute()
const router = useRouter()

const modal = ref(false)

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

const avatar = computed(() => {
  return createAvatar(identicon, { seed: state.user.username }).toDataUri()
})

const balance = computed(() => {
  const moneyFormat = new Intl.NumberFormat(locale.value, { style: 'currency', currency: 'USD' })
  if (state.portfolio.available.length === 0)
    return moneyFormat.format(0)
  return moneyFormat.format(state.portfolio.available[state.portfolio.active].balance_cents / 100)
})

function renderIcon(icon: Component) {
  return () => {
    return h(NIcon, null, {
      default: () => h(icon),
    })
  }
}

// redirect to login if not authenticated
watch(() => fintasy.authenticated.value, () => {
  if (!fintasy.authenticated.value)
    router.push('/login')
}, { immediate: true })

// get state on mount, manually refresh when needed
onMounted(() => {
  state.refresh.all()
})
</script>

<template>
  <n-layout-header bordered h-48px w-full flex>
    <div flex grow items-center gap-5 py-1>
      <!-- parent should be w-55 to match sidebar size -->
      <div hidden h-full w-55 items-center justify-center lg:flex>
        <Logo />
      </div>

      <!-- refresh button -->
      <n-tooltip>
        <template #trigger>
          <n-button text hidden lg:block @click="$router.go(0)">
            <NIcon size="20">
              <RefreshIcon />
            </NIcon>
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

      <!-- portfolio balance -->
      <div hidden w-fit items-center justify-center fn-outline px-2 op-85 md:flex>
        Balance: {{ balance }}
      </div>

      <!-- switch / create portfolio -->
      <div h-fit flex gap-2>
        <div w-fit cursor-pointer items-center justify-center fn-outline px-2 op-85 fn-hover>
          <n-dropdown
            :options="portfolios"
            trigger="click"
            @select="(key: any, option: any) => {
              state.portfolio.active = key
              message.info(`Switched to ${option.label}`)
            }"
          >
            <div gap-1>
              {{ portfolios.length > 0 ? portfolios[state.portfolio.active].label : 'None' }}
              <NIcon size="10">
                <DropdownIcon />
              </NIcon>
            </div>
          </n-dropdown>
        </div>
        <div
          flex cursor-pointer items-center fn-outline fn-hover
          @click="modal = true"
        >
          <NIcon size="20">
            <AddIcon />
          </NIcon>
        </div>
        <AddPortfolioModal v-model="modal" />
      </div>

      <!-- language switch -->
      <LanguageSwitch />

      <!-- theme switch -->
      <ThemeSwitch />

      <!-- notifications with badge -->
      <n-tooltip>
        <template #trigger>
          <n-button text @click="() => message.info(`Clicked notifications`)">
            <n-badge dot processing>
              <NIcon size="22">
                <BellIcon />
              </NIcon>
            </n-badge>
          </n-button>
        </template>
        Notifications
      </n-tooltip>

      <!-- user dropdown -->
      <n-dropdown
        :options="[
          { key: 0, label: state.user.username, icon: renderIcon(UserIcon), disabled: true },
          { key: 1, type: 'divider' },
          { key: 2, label: 'Logout', icon: renderIcon(LogoutIcon) },
        ]"
        trigger="click"
        @select="async (key: any, option: any) => {
          if (key === 2) {
            message.success('Logged out')
            await fintasy.logout()
          }
        }"
      >
        <n-avatar
          size="small"
          :src="avatar"
          mr-5 cursor-pointer
        />
      </n-dropdown>
    </div>
  </n-layout-header>
</template>
