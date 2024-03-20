<script setup lang="ts">
import type { ACTION, Transaction } from '~/types'

const { t } = useI18n()

useHead({
  title: `${t('pages.dashboard.title')} • Fintasy`,
})

interface Asset {
  symbol: string
  quantity: string
  pl_day: string
  pl_total: string
}

const cash = (Math.random() * 1500) + 500
const chartData = generateData(Math.floor(Math.random() * 1500) + 500)
const assets = generateAssets(Math.floor(Math.random() * 100) + 100)
const transactions = generateTransactions(Math.floor(Math.random() * 100) + 200)

// Generate random data
function generateData(count: number) {
  const data = []
  const startDate = new Date().getTime() - 1000 * 60 * 15 * count
  let value = 1000

  for (let i = 0; i < count; ++i) {
    value = Math.round((Math.random() * 1 - 0.495) * 100 + value)
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
      symbol: Math.random().toString(36).substring(2, 6).toUpperCase(),
      quantity: `x${Math.floor(Math.random() * 100).toString()}`,
      pl_day: `${(Math.random() * 1).toFixed(2)}%`,
      pl_total: `${(Math.random() * 50 - 20).toFixed(2)}%`,
    })
  }
  return assets
}

// Generate random transactions
function generateTransactions(count: number): Transaction[] {
  const transactions = []
  const date = new Date()

  for (let i = 0; i < count; ++i) {
    date.setTime(date.getTime() - Math.random() * 86400000)
    transactions.push({
      uuid: Math.random().toString(36).substring(2),
      portfolio: Math.random().toString(36).substring(2),
      symbol: Math.random().toString(36).substring(2, 6).toUpperCase(),
      action: Math.floor(Math.random() * 2) as ACTION,
      quantity: Math.floor(Math.random() * 100),
      price_cents: Math.floor(Math.random() * 100000),
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
      <div flex grow-3 flex-col fn-outline bg--c-fg p-2>
        <PortfolioAssets :assets="assets" :cash="cash" />
      </div>
    </div>
    <div flex grow flex-col fn-outline bg--c-fg p-2>
      <TransactionHistory :transactions="transactions" />
    </div>
  </div>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
