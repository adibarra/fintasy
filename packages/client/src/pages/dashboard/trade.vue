<!--
  @author: adibarra (Alec Ibarra), maclark (Mason Clark)
  @description: This component is used to display the trading page of the application.
-->

<script setup lang="ts">
import seedrandom from 'seedrandom'
import type { Quote } from '~/types'

const state = useStateStore()
const fintasy = useAPI()

const rng = seedrandom(state.user.username)
const trend = ref(generateData(Math.floor(rng() * 1500) + 500))
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

onMounted(async () => {
  quotes.value = await getQuotes()
})
</script>

<template>
  <!-- main wrapper div -->
  <div flex grow gap-3>
    <!-- left side div -->
    <div h-full w-26vw fn-outline bg--c-fg>
      <div m-8 fn-outline>
        <DataTable :quotes="quotes" />
      </div>
    </div>

    <!-- right side div -->
    <div grow fn-outline bg--c-fg p-10>
      <div h-80>
        <PortfolioChart :data="trend" />
      </div>
      <div grow py-15>
        <DataTable :quotes="quotes" />
      </div>
    </div>
  </div>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
