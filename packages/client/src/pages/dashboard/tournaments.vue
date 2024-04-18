<script lang="ts">
import { defineComponent, ref } from 'vue'

export default defineComponent({
  components: {
    TournamentFilters,
    TournamentsList,
  },
  setup() {
    const currentFilters = ref({})

    const applyFilters = (filters: any) => {
      currentFilters.value = { ...filters } // Ensuring reactivity by spreading into a new object
    }

    return {
      currentFilters,
      applyFilters,
    }
  },
})
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
