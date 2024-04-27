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

const quantity = ref(0)

const searchFilter = ref('')
const columns = [
  { key: 'symbol', label: 'Symbol' },
  { key: 'price', label: 'Price' },
  { key: 'quantity', label: 'Qty' },
  { key: 'action', label: 'Buy/Sell' },
]

const filteredQuotes = computed(() => {
  return props.quotes.filter((quote) => {
    return quote.symbol.toString().toLowerCase().includes(searchFilter.value.toLowerCase())
  })
})

function handleSearch(search: string) {
  searchFilter.value = search
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
          class="border-b font-900"
          flex
          @click="() => {
            emit('selected', quote)
          }"
        >
          <td class="px-2 py-2" w-12 grow text-center>
            {{ quote.symbol }}
          </td>
          <td class="px-2 py-2" w-15 grow text-center>
            {{ `$${(quote.price_cents / 100).toFixed(2)}` }}
          </td>
          <td class="px-2 py-2" w-15 grow text-center>
            <input
              v-model="quantity"
              type="text"
              placeholder="Qty"
              class="bg-gray-50 text-gray-900"
              w-15 fn-outline text-center
            >
          </td>
          <td class="px-2 py-2" w-15 grow text-center>
            <button
              class="mr-2 border bg-green-500 px-2 py-1 hover:bg-green-600"
              @click="createTransaction(quote, quantity, 'BUY' as ACTION)"
            >
              ✓
            </button>
            <button
              class="border bg-red-500 px-2 py-1 hover:bg-red-600"
              @click="createTransaction(quote, quantity, 'SELL' as ACTION)"
            >
              ✕
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
