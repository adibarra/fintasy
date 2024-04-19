<script setup lang="ts">
interface Item {
  symbol: string
  price_cents: number
}

const props = defineProps({
  items: {
    type: Object as PropType<Item[]>,
    required: true,
  },
})

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
          <td class="px-4 py-3">
            <button class="mr-2 border bg-green-500 px-2 py-1 hover:bg-green-600">
              ✓
            </button>
            <button class="border bg-red-500 px-2 py-1 hover:bg-red-600">
              ✕
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
