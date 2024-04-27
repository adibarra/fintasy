<!--
  @author: adibarra (Alec Ibarra), maclark (Mason Clark)
  @description: This component is used to display the data table in the trading page.
-->

<script setup lang="ts">
import { ACTION, type Quote } from '~/types'

const props = defineProps({
  assetMap: {
    type: Object as PropType<Record<string, number>>,
    required: true,
  },
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
  { key: 'owned', label: 'Owned' },
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

async function createTransaction(quote: Quote, quantity: number, action: ACTION) {
  const uuid = state.portfolio.available[state.portfolio.active].uuid
  await fintasy.createTransaction({
    portfolio: uuid,
    symbol: quote.symbol,
    action,
    quantity,
  })
  await state.refresh.transactions()
}
</script>

<template>
  <div>
    <div class="flex items-center">
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

      <div grow />

      <div class="flex items-center justify-end text-sm font-semibold">
        <FilterRadios @filter="handleRadioFilter" />
      </div>

      <div class="flex items-center justify-end">
        <FilterDropdown />
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
        flex border-b font-900 first:border-t
        @click="() => {
          emit('selected', quote)
          selected = quote
        }"
      >
        <td class="px-2 py-2" w-15 grow text-center>
          {{ quote.symbol }}
        </td>
        <td class="px-2 py-2" w-11 grow text-center>
          {{ `$${(quote.price_cents / 100).toFixed(2)}` }}
        </td>
        <td class="px-2 py-2" w-11 grow text-center>
          <input
            type="text"
            placeholder="Qty"
            class="bg-gray-50 text-gray-900"
            w-15 fn-outline text-center
          >
        </td>
        <td w-15 flex grow justify-center gap-2 p-1>
          <button
            b-1 bg-green-500 px-2 py-1 hover:bg-green-600
            @click="createTransaction(quote, 1, ACTION.BUY)"
          >
            ✓
          </button>
          <button
            b-1 bg-red-500 px-2 py-1 hover:bg-red-600
            @click="createTransaction(quote, 1, ACTION.SELL)"
          >
            ✕
          </button>
        </td><td class="px-2 py-2" w-15 grow text-center>
          {{ props.assetMap[quote.symbol] || 0 }}
        </td>
      </tr>
    </tbody>
  </table>
</template>
