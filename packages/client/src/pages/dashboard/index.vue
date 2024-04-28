<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the dashboard of the application.
-->

<script setup lang="ts">
import seedrandom from 'seedrandom'
import { ACTION } from '~/types'

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
const transactions = computed(() => state.transactions)
const chartData = computed(() => generateData(
  state.user.username,
  transactions.value.length > 0
    ? (new Date().getTime()
    - new Date(transactions.value[transactions.value.length - 1].created_at).getTime())
    / 1000 / 60 / 15
    : 0,
),
)
const assets = computed(() => {
  const rand = seedrandom(state.user.username)
  const assets: Asset[] = []
  transactions.value.forEach((transaction) => {
    const index = assets.findIndex(a => a.symbol === transaction.symbol)
    const quantity = transaction.action === ACTION.BUY ? transaction.quantity : -transaction.quantity
    if (index === -1) {
      assets.push({
        symbol: transaction.symbol,
        quantity,
        price_cents: transaction.price_cents,
        pl_day: 0,
        pl_total: 0,
      })
    }
    else {
      assets[index].quantity += quantity
    }
  })
  assets.forEach((asset) => {
    asset.pl_day = asset.quantity * asset.price_cents * (rand() * 0.01)
    asset.pl_total = asset.pl_day * 1.3
  })
  return assets
})

// generate random data
function generateData(seed: string, count: number) {
  const rand = seedrandom(seed)
  const data = []
  const startDate = new Date().getTime() - 1000 * 60 * 15 * count
  let value = 10000

  for (let i = 0; i < count - 1; i++) {
    data.push({
      date: startDate + 1000 * 60 * 15 * i,
      value,
    })
    value = Math.round((rand() * 1 - 0.4995) * 100 + value)
  }
  return data
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
