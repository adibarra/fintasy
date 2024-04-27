<script setup lang="ts">
import { SortAmountDownAlt as arrowDownIcon, SortAmountUp as arrowUpIcon } from '@vicons/fa'

const emit = defineEmits(['filter'])

function filter(e) {
  emit('filter', e.target.value)
}
</script>

<template>
  <label class="checked mr-4 flex flex-nowrap items-center gap-2" @change="filter">
    <input type="radio" name="show" value="hiLow">
    <span class="m1-1 whitespace-nowrap">
      <n-icon>
        <arrowUpIcon />
      </n-icon>
    </span>
  </label>
  <label class="mr-4 flex flex-nowrap items-center gap-2" @change="filter">
    <input type="radio" name="show" value="lowHi">
    <span class="m1-1 whitespace-nowrap">
      <n-icon>
        <arrowDownIcon />
      </n-icon>
    </span>
  </label>
</template>
