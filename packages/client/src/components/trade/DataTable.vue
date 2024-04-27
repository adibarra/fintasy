<script setup lang="ts">
import type { ACTION, Quote } from '~/types'

const props = defineProps({
  quotes: {
    type: Object as PropType<Quote[]>,
    required: true,
  },
})

const emit = defineEmits<{
  selected: [quote: Quote]
}>()

const state = useStateStore()
const fintasy = useAPI()

const selected = ref<Quote | null>(null)
const searchFilter = ref('')
const radioFilter = ref('')

const columns = [
  { key: 'symbol', label: 'Symbol' },
  { key: 'price', label: 'Price' },
  { key: 'quantity', label: 'Qty' },
  { key: 'action', label: 'Buy/Sell' },
]

const filteredQuotes = computed(() => {
  const items = props.quotes.toSorted((a: Quote, b: Quote) => {
    switch (radioFilter.value) {
      case 'hiLow':
        return b.price_cents - a.price_cents

      case 'lowHi':
        return a.price_cents - b.price_cents

      default:
        return 0
    }
  })

  return items.filter((quote) => {
    return quote.symbol.toString().toLowerCase().includes(searchFilter.value.toLowerCase())
  })
})

function handleSearch(search: string) {
  searchFilter.value = search
}

function handleRadioFilter(filter: string) {
  radioFilter.value = filter
}

function createTransaction(quote: Quote, quantity: number, action: ACTION) {
  const uuid = state.portfolio.available[state.portfolio.active].uuid
  fintasy.createTransaction({
    portfolio: uuid,
    symbol: quote.symbol,
    action,
    quantity,
  })
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between">
      <div mx-2 my-2>
        <input
          type="text"
          placeholder="Search"
          class="bg-gray-50 pl-2 text-gray-900"
          grow fn-outline
          @input="(e) => {
            const target = e.target as HTMLInputElement
            handleSearch(target.value)
          }"
        >
      </div>

      <div class="flex items-center justify-end text-sm font-semibold">
        <FilterRadios @filter="handleRadioFilter" />
      </div>
    </div>
  </div>

  <table class="flex flex-col text-sm">
    <thead class="text-xs uppercase">
      <tr flex>
        <template
          v-for="column in columns"
          :key="column.key"
        >
          <th class="px-2 py-2" grow>
            {{ column.label }}
          </th>
        </template>
      </tr>
    </thead>

    <tbody>
      <tr
        v-for="quote in filteredQuotes"
        :key="quote.symbol"
        :class="{ 'bg--c-accent text--c-bg': selected === quote }"
        flex border-b font-900
        @click="() => {
          emit('selected', quote)
          selected = quote
        }"
      >
        <td w-12 grow px-2 py-2 text-center>
          {{ quote.symbol }}
        </td>
        <td w-15 grow px-2 py-2 text-center>
          {{ `$${(quote.price_cents / 100).toFixed(2)}` }}
        </td>
        <td w-15 grow px-2 py-2 text-center>
          <input
            type="text"
            placeholder="Qty"
            class="bg-gray-50 text-gray-900"
            w-15 fn-outline text-center
          >
        </td>
        <td w-15 grow px-2 py-2 text-center>
          <button
            mr-2 b-1 bg-green-500 px-2 py-1 hover:bg-green-600
            @click="createTransaction(quote, 0, 'BUY' as ACTION)"
          >
            ✓
          </button>
          <button
            b-1 bg-red-500 px-2 py-1 hover:bg-red-600
            @click="createTransaction(quote, 0, 'SELL' as ACTION)"
          >
            ✕
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>
