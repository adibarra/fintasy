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
.filters {
  background-color: #202020; /* Dark background for the filter area */
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 8px; /* Rounded corners */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow */
}

.filters input,
.filters select,
.n-date-picker {
  background-color: #202020; /* Dark background for all inputs */
  color: #fff; /* White text color for contrast */
  margin-bottom: 8px;
  width: 100%; /* Full-width inputs */
  padding: 8px;
  border: 1px solid #ddd; /* Subtle border for inputs */
  border-radius: 4px; /* Rounded corners for inputs */
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05); /* Inset shadow */
}

.filters input:focus,
.filters select:focus,
.n-date-picker:focus {
  border-color: #0056b3; /* Blue border for focused elements */
  outline: none;
}

.filters select {
  appearance: none; /* Custom appearance for dropdown */
  background-image: url('data:image/svg+xml;charset=US-ASCII,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4 5"><path fill="%230056b3" d="M2 0L0 2h4L2 0zm0 5L0 3h4l-2 2z"/></svg>');
  background-repeat: no-repeat;
  background-position: right 8px center; /* Position of custom arrow */
  background-size: 10px;
  cursor: pointer;
}

.n-date-picker {
  background-color: #202020; /* Ensuring background is consistently black */
  color: #fff; /* Ensuring text color is white for readability */
}

.filters > div {
  display: flex;
  flex-direction: column;
}
</style>
