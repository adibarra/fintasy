<script setup lang="ts">
import type { STATUS } from '~/types'

interface TournamentFilter {
  owner?: string
  name?: string
  status?: STATUS
  start_date?: Date
  end_date?: Date
}

const currentFilters = ref<TournamentFilter>({
  owner: undefined,
  name: undefined,
  status: undefined,
  start_date: undefined,
  end_date: undefined,
})

function applyFilters(filters: any) {
  // Ensuring reactivity by spreading into a new object
  currentFilters.value = { ...filters }
}
</script>

<template>
  <div h-full w-full flex flex-col gap-2 xl:flex-row>
    <div
      class="filter-section"
      fn-outline bg--c-fg p-4
    >
      <TournamentFilters @filter="applyFilters" />
    </div>
    <div
      class="tournaments-section"
      fn-outline bg--c-fg p-4
    >
      <TournamentsList :filters="currentFilters" />
    </div>
  </div>
</template>

<style>
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
