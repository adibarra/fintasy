<!--
  @author: adibarra (Alec Ibarra), maclark (Mason Clark)
  @description: This component is used to display the trading page of the application.
-->

<script setup lang="ts">
import seedrandom from 'seedrandom'
import { ACTION, type Quote } from '~/types'

const state = useStateStore()
const fintasy = useAPI()

const assetQtyMap = computed<Record<string, number>>(() => {
  const map: Record<string, number> = {}
  state.transactions.forEach((transaction) => {
    const symbol = transaction.symbol
    const quantity = transaction.quantity * (transaction.action === ACTION.BUY ? 1 : -1)
    symbol in map ? map[symbol] += quantity : map[symbol] = quantity
  })
  return map
})
const loading = ref(false)
const currentSymbol = ref(`${state.user.username.toUpperCase()}'s Portfolio`)
const trend = ref(generateData(state.user.username, 2000))
const quotes = ref<Quote[]>([])
const availableSymbols = ref<string[]>([
  'AAPL',
  'ADBE',
  'AMC',
  'AMD',
  'AMZN',
  'BBW',
  'GME',
  'GOOGL',
  'JPM',
  'META',
  'MSFT',
  'NFLX',
  'NIO',
  'NVDA',
  'PYPL',
  'RACE',
  'TSLA',
  'TWNK',
  'TWTR',
])

// get quotes for available symbols
async function getQuotes() {
  const quotes: Quote[] = []

  loading.value = true
  const quotePromises = availableSymbols.value.map(async (symbol) => {
    const response = await fintasy.getQuote({ symbol })
    if (response.code === 200)
      return response.data

    return undefined
  })

  const resolvedQuotes = await Promise.all(quotePromises)
  loading.value = false

  resolvedQuotes.forEach((quote) => {
    if (quote !== undefined)
      quotes.push(quote)
  })

  return quotes
}

// generate random test data
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

onMounted(async () => {
  quotes.value = await getQuotes()
  await state.refresh.transactions()
})
</script>

<template>
  <!-- main wrapper div -->

  <!-- right side div -->
  <div flex grow flex-col fn-outline bg--c-fg p-10>
    <div mb-20 h-80 sm:mb-12>
      <PortfolioChart
        :name="currentSymbol.length > 6 ? currentSymbol : `${currentSymbol} Trend`"
        :data="trend"
      />
    </div>
    <div flex grow>
      <div v-if="loading" flex grow items-center justify-center>
        <n-spin />
      </div>
      <div v-else grow>
        <DataTable
          :asset-map="assetQtyMap"
          :quotes="quotes"
          @selected="quote => {
            trend = generateData(quote.symbol, 2000)
            currentSymbol = quote.symbol
          }"
        />
      </div>
    </div>
  </div>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
