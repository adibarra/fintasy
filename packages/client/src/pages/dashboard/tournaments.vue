<script setup lang="ts">
import type { STATUS } from '~/types'

interface filter {
  owner: string | undefined
  name: string | undefined
  status: STATUS | undefined
  dateTimeRange: [Date, Date] | undefined
}

const currentFilters = ref<filter>({
  owner: undefined,
  name: undefined,
  status: undefined,
  dateTimeRange: undefined,
})

function applyFilters(filters: any) {
  currentFilters.value = { ...filters } // Ensuring reactivity by spreading into a new object
}
</script>

<template>
  <div class="app">
    <div class="filter-section">
      <TournamentFilters @filter="applyFilters" />
    </div>
    <div class="tournaments-section">
      <TournamentsList :filters="currentFilters" />
    </div>
  </div>
</template>

<style>
.app {
  display: flex;
}
.filter-section {
  flex: 1;
}
.tournaments-section {
  flex: 3;
}
</style>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
