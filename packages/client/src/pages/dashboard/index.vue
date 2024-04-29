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
  avg_price_cents: number
  pl_total: number
}

const cash = computed(() => {
  if (state.portfolio.available.length === 0)
    return 0
  const balance_cents = state.portfolio.available[state.portfolio.active].balance_cents
  return (balance_cents / 100)
})
const transactions = computed(() => state.transactions)
const startTime = computed(() => {
  if (state.portfolio.available.length < state.portfolio.active + 1)
    return new Date().getTime()
  return new Date(state.portfolio.available[state.portfolio.active].created_at).getTime()
})
const deltaTime = ref(0)

const chartData = computed(() => generateData(
  state.user.username,
  deltaTime.value,
  startTime.value,
))
const assets = computed(() => {
  const assets: Asset[] = []
  transactions.value.forEach((transaction) => {
    const index = assets.findIndex(a => a.symbol === transaction.symbol)
    const quantity = transaction.action === ACTION.BUY ? transaction.quantity : -transaction.quantity
    if (index === -1) {
      assets.push({
        symbol: transaction.symbol,
        quantity: transaction.quantity,
        price_cents: transaction.price_cents / transaction.quantity,
        avg_price_cents: transaction.price_cents / transaction.quantity,
        pl_total: 0,
      })
    }
    else {
      assets[index].quantity += quantity
      assets[index].price_cents = transaction.price_cents / transaction.quantity
      assets[index].avg_price_cents += transaction.price_cents
    }
  })
  assets.forEach((asset) => {
    if (asset.quantity === 0)
      return
    asset.avg_price_cents /= asset.quantity
    asset.pl_total = (asset.price_cents - asset.avg_price_cents) * asset.quantity
    asset.quantity = transactions.value.filter(t => t.symbol === asset.symbol).reduce((acc, t) => {
      return t.action === ACTION.BUY ? acc + t.quantity : acc - t.quantity
    }, 0)
  })
  return assets.filter(asset => asset.quantity > 0)
})

// update chart data every 2 seconds
setInterval(() => {
  deltaTime.value = Math.floor((new Date().getTime() - startTime.value) / 1000)
}, 2000)

// generate random data
function generateData(seed: string, count: number, startDate: number) {
  const rand = seedrandom(seed)
  const data = []
  const endDate = new Date().getTime()

  if (count > 10000)
    count /= 100
  else if (count > 1000)
    count /= 10

  const interval = Math.floor((endDate - startDate) / count)
  let date = startDate
  let value = 10000

  for (let i = 0; i < count; ++i) {
    data.push({ date, value })

    date += interval

    // if user has no transactions, don't change value
    if (transactions.value.length === 0)
      continue

    // if date is before when user made their first transaction, don't change value
    if (date < new Date(transactions.value[transactions.value.length - 1].created_at).getTime())
      continue

    // if date is when stock market is closed, don't change value
    if (new Date(date).getUTCHours() < 13 || new Date(date).getUTCHours() > 20)
      continue

    // if date is on a weekend, don't change value
    if (new Date(date).getUTCDay() === 0 || new Date(date).getUTCDay() === 6)
      continue

    value = Math.round((rand() * 1 - 0.49995) * 5 + value)
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
