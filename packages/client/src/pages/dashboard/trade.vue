<!--
  @author: adibarra (Alec Ibarra), maclark (Mason Clark)
  @description: This component is used to display the trading page of the application.
-->

<script setup lang="ts">
import seedrandom from 'seedrandom'
import type { Quote } from '~/types'

const state = useStateStore()
const fintasy = useAPI()

const currentSymbol = ref(`${state.user.username}'s Portfolio`)
const trend = ref(generateData(state.user.username, 2000))
const quotes = ref<Quote[]>([])
const availableSymbols = ref<string[]>([
  'AAPL',
  'GOOGL',
  'AMZN',
  'MSFT',
  'TSLA',
  'FB',
  'NVDA',
  'PYPL',
  'INTC',
  'ADBE',
])

// get quotes for available symbols
async function getQuotes() {
  const quotes: Quote[] = []

  const quotePromises = availableSymbols.value.map(async (symbol) => {
    const response = await fintasy.getQuote({ symbol })
    if (response.code === 200)
      return response.data

    return undefined
  })

  const resolvedQuotes = await Promise.all(quotePromises)

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
})
</script>

<template>
  <!-- main wrapper div -->

  <!-- right side div -->
  <div grow fn-outline bg--c-fg p-10>
    <div h-80>
      <PortfolioChart
        :name="`${currentSymbol} Trend`"
        :data="trend"
      />
    </div>
    <div grow py-15>
      <DataTable
        :quotes="quotes"
        @selected="quote => {
          trend = generateData(quote.symbol, 2000)
          currentSymbol = quote.symbol
        }"
      />
    </div>
  </div>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
