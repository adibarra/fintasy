<!--
  @author: maclark (Mason Clark)
  @description: This component is used to display the filter radios in the trading page.
-->

<script setup lang="ts">
import {
  SortAmountDownAlt as ArrowDownIcon,
  SortAmountUp as ArrowUpIcon,
} from '@vicons/fa'

const emit = defineEmits(['filter'])

function filter(e: any) {
  emit('filter', e.target.value)
}
</script>

<template>
  <label class="checked mr-4 flex flex-nowrap items-center gap-2" @change="filter">
    <input type="radio" name="show" value="hiLow">
    <span class="m1-1 whitespace-nowrap">
      <n-icon>
        <ArrowUpIcon />
      </n-icon>
    </span>
  </label>
  <label class="mr-4 flex flex-nowrap items-center gap-2" @change="filter">
    <input type="radio" name="show" value="lowHi">
    <span class="m1-1 whitespace-nowrap">
      <n-icon>
        <ArrowDownIcon />
      </n-icon>
    </span>
  </label>
</template>
