<!--
  @author: adibarra (Alec Ibarra), maclark (Mason Clark)
  @description: This component is used to display the data table in the trading page.
-->

<script setup lang="ts">
import type { Quote } from '~/types'

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

const selected = ref<Quote | null>(null)
const searchFilter = ref('')
const radioFilter = ref('')
const filterValue = ref('All')

const columns = [
  { key: 'symbol', label: 'Symbol' },
  { key: 'price', label: 'Price' },
  { key: 'quantity', label: 'Qty' },
  { key: 'action', label: 'Buy/Sell' },
  { key: 'owned', label: 'Owned' },
]

const filteredQuotes = computed(() => {
  const map = props.assetMap as Record<string, number>

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
    return ownedFilter(map, quote) && quote.symbol.toString().toLowerCase()
      .includes(searchFilter.value.toLowerCase())
  })
})

function ownedFilter(assetMap: Record<string, number>, quote: Quote) {
  switch (filterValue.value) {
    case 'Owned':
      return assetMap[quote.symbol] > 0

    case 'Not Owned':
      return assetMap[quote.symbol] === 0

    default:
      return true
  }
}

function handleSearch(search: string) {
  searchFilter.value = search
}

function handleRadioFilter(filter: string) {
  radioFilter.value = filter
}
</script>

<template>
  <div>
    <div class="flex items-center">
      <input
        type="text"
        placeholder="Search"
        my-2 max-w-50 grow fn-outline bg--c-fg py-0.5 pl-2 text--c-inverse
        @input="(e) => {
          const target = e.target as HTMLInputElement
          handleSearch(target.value)
        }"
      >

      <div grow />

      <div class="flex items-center justify-end text-sm font-semibold">
        <FilterRadios @filter="handleRadioFilter" />
      </div>

      <div class="flex items-center justify-end">
        <FilterDropdown v-model="filterValue" />
      </div>
    </div>
  </div>

  <table class="flex flex-col text-sm" fn-outline>
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
        flex border-b font-900 first:border-t last:border-b-none
        @click="() => {
          emit('selected', quote)
          selected = quote
        }"
      >
        <DataTableRow
          :asset-map="assetMap"
          :quote="quote"
        />
      </tr>
    </tbody>
  </table>
</template>
