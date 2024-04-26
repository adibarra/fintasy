<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the dashboard of the application.
-->

<script setup lang="ts">
import seedrandom from 'seedrandom'
import type { Transaction } from '~/types'
import { ACTION } from '~/types'

const { t } = useI18n()
const state = useStateStore()
const fintasy = useAPI()
const rng = seedrandom(state.user.username)

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

const cash = (rng() * 1500) + 500
const chartData = generateData(Math.floor(rng() * 1500) + 500)
const assets = generateAssets(Math.floor(rng() * 100) + 100)
const transactions = generateTransactions(Math.floor(rng() * 100) + 200)

// Generate random data
function generateData(count: number) {
  const data = []
  const startDate = new Date().getTime() - 1000 * 60 * 15 * count
  let value = 1000

  for (let i = 0; i < count; ++i) {
    value = Math.round((rng() * 1 - 0.495) * 100 + value)
    data.push({
      date: startDate + 1000 * 60 * 15 * i,
      value,
    })
  }
  return data
}

// Generate random assets
function generateAssets(count: number): Asset[] {
  const assets = []

  for (let i = 0; i < count; ++i) {
    assets.push({
      symbol: rng().toString(36).substring(2, 6).toUpperCase(),
      quantity: Math.floor(rng() * 100),
      price_cents: rng() * 10000 + 2500,
      pl_day: rng() * 2500 + 1000,
      pl_total: rng() * 5000 + 1000,
    })
  }
  return assets
}

// Generate random transactions
function generateTransactions(count: number): Transaction[] {
  const transactions = []
  const date = new Date()

  for (let i = 0; i < count; ++i) {
    date.setTime(date.getTime() - rng() * 86400000)
    transactions.push({
      uuid: rng().toString(36).substring(2),
      portfolio: rng().toString(36).substring(2),
      symbol: rng().toString(36).substring(2, 6).toUpperCase(),
      action: rng() > 0.5 ? ACTION.BUY : ACTION.SELL,
      quantity: Math.floor(rng() * 100),
      price_cents: Math.floor(rng() * 100000),
      created_at: date.toLocaleDateString(),
    })
  }
  return transactions
}
</script>

<template>
  <div h-full w-full flex flex-col gap-2 xl:flex-row>
    <div flex grow flex-col gap-2>
      <div flex grow-1 flex-col fn-outline bg--c-fg p-2>
        <PortfolioChart :data="chartData" />
      </div>
      <div flex grow-3 flex-col fn-outline bg--c-fg p-2 max-xl:h-122>
        <PortfolioAssets :assets="assets" :cash="cash" />
      </div>
    </div>
    <div flex grow flex-col fn-outline bg--c-fg p-2 max-xl:h-205>
      <TransactionHistory :transactions="transactions" />
    </div>
  </div>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
