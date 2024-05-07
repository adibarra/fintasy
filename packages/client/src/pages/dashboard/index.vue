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
    return 0
  return new Date(state.portfolio.available[state.portfolio.active].created_at).getTime() - new Date().getTimezoneOffset() * 60000
})
const deltaTime = ref(0)

const chartData = computed(() => generateData(
  state.user.username,
  deltaTime.value,
  startTime.value,
))
const assets = computed(() => {
  const assets: Asset[] = []
  const symbols: string[] = []

  if (transactions.value.length === 0)
    return assets

  transactions.value.forEach((transaction) => {
    if (!symbols.includes(transaction.symbol))
      symbols.push(transaction.symbol)
  })

  symbols.forEach((symbol) => {
    const symbol_transactions = transactions.value.filter(t => t.symbol === symbol)
    const owned = symbol_transactions.reduce((acc, t) => {
      return t.action === ACTION.BUY ? acc + t.quantity : acc - t.quantity
    }, 0)

    if (owned === 0)
      return

    const price_cents = symbol_transactions[0].price_cents / symbol_transactions[0].quantity
    const tot_price_cents = symbol_transactions.reduce((acc, t) => {
      return t.action === ACTION.BUY ? acc + t.price_cents : acc - t.price_cents
    }, 0)
    const avg_price_cents = tot_price_cents / owned
    const pl_total = (price_cents - avg_price_cents) * owned

    assets.push({
      symbol,
      quantity: owned,
      price_cents,
      avg_price_cents,
      pl_total,
    })
  })

  return assets
})

function generateData(seed: string, count: number, startDate: number) {
  if (count === 0 || startDate === 0)
    return []

  if (count > 10000)
    count = 10000

  const rand = seedrandom(seed)
  const data = []
  const endDate = new Date().getTime()

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
    if (new Date(date).getUTCHours() < 11 || new Date(date).getUTCHours() > 18)
      continue

    // if date is on a weekend, don't change value
    if (new Date(date).getUTCDay() === 0 || new Date(date).getUTCDay() === 6)
      continue

    value = Math.round((rand() * 1 - 0.49995) * 5 + value)
  }
  return data
}

onMounted(() => {
  // update chart data every 2 seconds
  setInterval(() => {
    deltaTime.value = Math.floor((new Date().getTime() - startTime.value) / 1000)
  }, 2000)
})
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
