<script setup>
import { computed, defineProps, ref } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    required: true,
  },
})

const searchFilter = ref('')

const filteredItems = computed(() => {
  if (searchFilter.value !== '') {
    return props.items.filter(item =>
      item.id.toString().toLowerCase().includes(searchFilter.value.toLowerCase()),
    )
  }
  return props.items
})

function handleSearch(search) {
  searchFilter.value = search
}
</script>

<template>
  <div class="relative border bg-emerald">
    <div class="flex items-center justify-between">
      <SearchForm @search="handleSearch" />

      <div class="flex items-center justify-end text-sm font-semibold">
        <FilterRadios />
        <FilterDropdown />
      </div>
    </div>

    <table class="w-full text-left text-sm text-white">
      <thead class="bg-gray-500 text-xs text-white uppercase">
        <tr>
          <th class="px-4 py-3">
            ID
          </th>
          <th class="px-4 py-3">
            Price
          </th>
          <th class="px-4 py-3">
            <span class="sr-only">Actions</span>Buy/Sell
          </th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="item in filteredItems" :key="item.id" class="border-b">
          <td class="px-4 py-3 text-white font-medium">
            {{ item.id }}
          </td>
          <td class="px-4 py-3 text-white font-medium">
            {{ item.price }}
          </td>
          <td class="px-4 py-3">
            <button class="mr-2 border bg-green-500 px-2 py-1 text-white hover:bg-green-600">
              ✔️
            </button>
            <button class="border bg-red-500 px-2 py-1 text-white hover:bg-red-600">
              ❌
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
