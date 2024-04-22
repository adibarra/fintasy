<script setup lang="ts">
import type { ACTION } from '~/types'

const props = defineProps({
  items: {
    type: Object as PropType<Item[]>,
    required: true,
  },
})
const fintasy = useAPI()
const symbol = ref('')
const price = ref(0)
const timeStamp = ref('')
const state = useStateStore()
const quantity = ref(0)

interface Item {
  symbol: string
  price_cents: number
}

// const pagination = ref({
//   page: 1,
//   pageSlot: 6,
//   itemsPerPage: 7,
//   itemCount: props.items.length,
// })
const searchFilter = ref('')
const columns = [
  { key: 'symbol', label: 'Symbol' },
  { key: 'price', label: 'Price' },
  { key: 'action', label: 'Buy/Sell' },
]

const filteredItems = computed(() => {
  return props.items.filter((item) => {
    return item.symbol.toString().toLowerCase().includes(searchFilter.value.toLowerCase())
  })
})

function handleSearch(search: string) {
  searchFilter.value = search
}

function quantitySetter(qty: string) {
  quantity.value = Number.parseInt(qty)
}

function initializeTransaction(action: ACTION) {
  const portfolioUID = state.portfolio.available[state.portfolio.active].uuid
  fintasy.createTransaction({
    portfolio: portfolioUID,
    symbol: symbol.value,
    action,
    quantity: quantity.value,
  })
}

onMounted(async () => {
  const response = await fintasy.getQuote({ symbol: searchFilter.value })
  if (response.code === 200) {
    symbol.value = response.data.symbol
    price.value = response.data.price_cents
    timeStamp.value = response.data.timestamp
  }
  else {
    console.log('Error fetching data')
  }
})
</script>

<template>
  <div class="bg-emerald">
    <div class="flex items-center justify-between">
      <SearchForm @search="handleSearch" />

      <div class="flex items-center justify-end text-sm font-semibold">
        <FilterRadios />
        <FilterDropdown />
      </div>
    </div>

    <table class="w-full text-left text-sm">
      <thead class="bg-gray-500 text-xs uppercase">
        <tr>
          <template
            v-for="column in columns"
            :key="column.key"
          >
            <th class="px-4 py-3">
              {{ column.label }}
            </th>
          </template>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="item in filteredItems"
          :key="item.symbol"
          class="border-b font-900"
        >
          <td class="px-4 py-3">
            {{ item.symbol }}
          </td>
          <td class="px-4 py-3">
            {{ `$${(item.price_cents / 100).toFixed(2)}` }}
          </td>
          <td>
            <form class="flex items-center px-4 py-3">
              <input
                type="text"
                placeholder="Quantity"
                class="bg-gray-50 pl-2 text-gray-900"
                grow
                fn-outline @input="quantitySetter($event.target.value as string)"
              >
            </form>
          </td>
          <td class="px-4 py-3">
            <button class="mr-2 border bg-green-500 px-2 py-1 hover:bg-green-600" @click="initializeTransaction('BUY' as ACTION)">
              ✓
            </button>
            <button class="border bg-red-500 px-2 py-1 hover:bg-red-600" @click="initializeTransaction('SELL' as ACTION)">
              ✕
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
