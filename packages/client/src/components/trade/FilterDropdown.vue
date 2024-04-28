<!--
  @author: maclark (Mason Clark)
  @description: This component is used to display the filter dropdown in the trading page.
-->

<script setup lang="ts">
const props = defineProps({
  items: {
    type: Object as PropType<Record<string, number>>,
    required: true,
  },
})

const show = ref(false)

const status = computed(() => {
  return Object.keys(props.items)
})
</script>

<template>
  <div class="relative w-full flex items-center px-4">
    <button class="text-white-900 w-full flex items-center justify-center border rounded-lg px-4 py-2 text-sm font-medium" @click="show = !show">
      Filter
    </button>
    <div v-if="show" class="absolute right-0 top-12 z-10 w-48 rounded-lg bg-gray-50 p-3 shadow-emerald">
      <h6 class="mb-3 text-sm text-gray-900 font-medium">
        Status
      </h6>
      <u1 class="text-sm space-y-2">
        <li>
          <input id="filter_option_${index}" type="checkbox" :value="status" class="h-4 w-4 bg-gray">
          <label for="filter_option_${index}" class="ml-2 text-gray-900 font-medium">
            {{ status }}
          </label>
        </li>
      </u1>
    </div>
  </div>
</template>
