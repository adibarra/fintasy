<!--
  @author: maclark (Mason Clark)
  @description: This component is used to display the filter dropdown in the trading page.
-->

<script setup lang="ts">
const modelValue = defineModel<string>()
const filterOptions = ref([
  { label: 'All', value: 'All' },
  { label: 'Owned', value: 'Owned' },
  { label: 'Not Owned', value: 'Not Owned' },
])
</script>

<template>
  <n-popselect v-model:value="modelValue" :options="filterOptions">
    <n-button>{{ modelValue || 'Filters' }}</n-button>
  </n-popselect>
</template>
