<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.dashboard.title')} • Fintasy`,
})

interface Transaction {
  uuid: string
  portfolio: string
  symbol: string
  action: string
  quantity: number
  price_cents: number
  created_at: string
}

interface Asset {
  symbol: string
  quantity: number | string
  pl_day: number | string
  pl_total: number | string
}

const chartData = generateData(1987)
const assets = generateAssets(123)
const transactions = generateTransactions(123)

// Generate random data
function generateData(count: number) {
  const data = []
  const date = new Date()
  let value = 1000

  date.setHours(0, 0, 0, 0)
  for (let i = 0; i < count; ++i) {
    value = Math.round((Math.random() * 1 - 0.495) * 100 + value)
    date.setTime(date.getTime() + 86400000)
    data.push({
      date: date.getTime(),
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
      symbol: Math.random().toString(36).substring(2),
      quantity: Math.floor(Math.random() * 100),
      pl_day: (Math.random() * 1).toFixed(2),
      pl_total: (Math.random() * 50 - 20).toFixed(2),
    })
  }
  return assets
}

// Generate random transactions
function generateTransactions(count: number): Transaction[] {
  const transactions = []
  const symbols = ['APPL', 'MSFT', 'AMZN']
  const actions = ['BUY', 'SELL']
  const date = new Date()

  for (let i = 0; i < count; ++i) {
    date.setTime(date.getTime() + Math.random() * 86400000)
    transactions.push({
      uuid: Math.random().toString(36).substring(2),
      portfolio: Math.random().toString(36).substring(2),
      symbol: symbols[Math.floor(Math.random() * symbols.length)],
      action: actions[Math.floor(Math.random() * actions.length)],
      quantity: Math.floor(Math.random() * 100),
      price_cents: Math.floor(Math.random() * 100000),
      created_at: date.toISOString(),
    })
  }
  return transactions
}
</script>

<template>
  <div id="widget area" h-full w-full flex flex-col gap-1 lg:flex-row>
    <div id="left area" flex grow flex-col gap-1>
      <div flex flex-col fn-outline bg--c-bg-secondary p-2>
        <PortfolioChart :data="chartData" />
      </div>
      <div flex grow flex-col fn-outline bg--c-bg-secondary p-2>
        <PortfolioAssets :assets="assets" />
      </div>
    </div>
    <div flex grow flex-col fn-outline bg--c-bg-secondary p-2 lg:w-120 lg:grow-0>
      <TransactionHistory :transactions="transactions" />
    </div>
  </div>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
