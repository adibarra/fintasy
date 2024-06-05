<!--
  @author: Zedfoura (Tinatsei Chingaya)
  @description: This component is used to display the filters for the tournaments page of the application.
-->

<script setup lang="ts">
import { ref, watch } from 'vue'
import { STATUS } from '~/types'

interface TournamentFilter {
  owner?: string
  name?: string
  status?: STATUS
  start_date?: Date | null
  end_date?: Date | null
}

const emit = defineEmits(['filter'])
const filters = ref<TournamentFilter>({
  name: undefined,
  owner: undefined,
  status: undefined,
  start_date: null,
  end_date: null,
})

// Watch the filters object to emit changes
watch(filters, (newFilters) => {
  emit('filter', newFilters)
}, { deep: true })

// Update function handles direct input from the date range picker
function updateDateRange([start, end]: [Date | null, Date | null]) {
  filters.value.start_date = start
  filters.value.end_date = end
}
</script>

<template>
  <div class="filters">
    <h2>Filters</h2>
    <div>
      <input v-model="filters.name" placeholder="Tournament Name">
      <input v-model="filters.owner" placeholder="Owner">

      <!-- Directly bind start_date and end_date -->
      <n-date-picker
        :model-value="[filters.start_date, filters.end_date]"
        type="datetimerange"
        clearable
        @update:model-value="updateDateRange"
      />

      <select v-model="filters.status">
        <option :value="undefined">
          All
        </option>
        <option :value="STATUS.SCHEDULED">
          Scheduled
        </option>
        <option :value="STATUS.ONGOING">
          On-going
        </option>
        <option :value="STATUS.FINISHED">
          Finished
        </option>
      </select>
    </div>
  </div>
</template>

<style scoped>
.filters form {
  display: flex;
  flex-direction: column;
}
.filters input,
.filters select {
  margin-bottom: 8px;
}
</style>
