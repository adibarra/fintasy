<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the dashboard of the application.
-->

<script setup lang="ts">
import seedrandom from 'seedrandom'

const { t } = useI18n()
const state = useStateStore()

useHead({
  title: `${t('pages.dashboard.title')} • Fintasy`,
})

interface Asset {
  symbol: string
  quantity: number
  price_cents: number
  pl_day: number
  pl_total: number
}

const cash = computed(() => {
  if (state.portfolio.available.length === 0)
    return 0
  const balance_cents = state.portfolio.available[state.portfolio.active].balance_cents
  return (balance_cents / 100)
})
const chartData = generateData(state.user.username, 2000)
const assets = generateAssets(state.user.username, 24)
const transactions = computed(() => state.transactions)

// generate random data
function generateData(seed: string, count: number) {
  const rand = seedrandom(seed)
  const data = []
  const startDate = new Date().getTime() - 1000 * 60 * 15 * count
  let value = 1000

  for (let i = 0; i < count; ++i) {
    value = Math.round((rand() * 1 - 0.495) * 100 + value)
    data.push({
      date: startDate + 1000 * 60 * 15 * i,
      value,
    })
  }
  return data
}

// generate random assets
function generateAssets(seed: string, count: number): Asset[] {
  const rand = seedrandom(seed)
  const assets = []

  for (let i = 0; i < count; ++i) {
    assets.push({
      symbol: rand().toString(36).substring(2, 6).toUpperCase(),
      quantity: Math.floor(rand() * 100),
      price_cents: rand() * 10000 + 2500,
      pl_day: rand() * 2500 + 1000,
      pl_total: rand() * 5000 + 1000,
    })
  }
  return assets
}
</script>

<template>
  <div h-full w-full flex flex-col gap-2 xl:flex-row>
    <div flex grow flex-col gap-2>
      <div flex grow-1 flex-col fn-outline bg--c-fg p-2>
        <PortfolioChart
          :name="t('pages.dashboard.portfolio-value')"
          :data="chartData"
        />
      </div>
      <div flex grow-3 flex-col fn-outline bg--c-fg p-2 max-xl:h-122>
        <PortfolioAssets
          :name="t('pages.dashboard.assets')"
          :assets="assets"
          :cash="cash"
        />
      </div>
    </div>
    <div flex grow flex-col fn-outline bg--c-fg p-2 max-xl:h-205>
      <TransactionHistory
        :name="t('pages.dashboard.history')"
        :transactions="transactions"
      />
    </div>
  </div>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
