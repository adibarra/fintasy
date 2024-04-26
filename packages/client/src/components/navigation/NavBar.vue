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
} from '@vicons/ionicons5'
import { NIcon, useMessage } from 'naive-ui'
import { createAvatar } from '@dicebear/core'
import { identicon } from '@dicebear/collection'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const message = useMessage()
const state = useStateStore()
const fintasy = useAPI()

const addPortfolioModal = ref(false)

function renderIcon(icon: Component) {
  return () => {
    return h(NIcon, null, {
      default: () => h(icon),
    })
  }
}

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
  return createAvatar(identicon, { seed: state.user.username }).toDataUriSync()
})

// redirect to login if not authenticated
watch(() => fintasy.authenticated.value, () => {
  if (!fintasy.authenticated.value)
    router.push('/login')
}, { immediate: true })

// get state on mount, manually refresh when needed
onMounted(() => {
  state.refresh.user()
  state.refresh.portfolio()
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

      <!-- coins -->
      <div hidden w-fit items-center justify-center fn-outline px-2 op-85 md:flex>
        Coins: 🪙 {{ state.user.coins }}
      </div>

      <!-- switch user portfolio account -->
      <div hidden h-fit gap-2 sm:flex>
        <div w-fit cursor-pointer items-center justify-center fn-outline px-2 op-85 fn-hover>
          <n-dropdown
            :options="portfolios"
            trigger="click"
            @select="(key: any, option: any) => {
              state.portfolio.active = key
              message.info(`Selected ${option.label}`)
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
          @click="addPortfolioModal = true"
        >
          <NIcon size="20">
            <AddIcon />
          </NIcon>
        </div>
        <NavAddPortfolio v-model="addPortfolioModal" />
      </div>

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
          { label: 'Logout', key: 0, icon: renderIcon(LogoutIcon) },
        ]"
        trigger="click"
        @select="(key: any, option: any) => {
          message.info(`Selected ${option.label}`)
          if (key === 0)
            fintasy.logout()
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
