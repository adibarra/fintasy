<script setup lang="ts">
import { STATUS } from '~/types'

interface filter {
  owner: string | undefined
  name: string | undefined
  status: STATUS | undefined
  dateTimeRange: [Date, Date] | undefined
}

const emit = defineEmits(['filter'])
const filters = ref<filter>({
  name: undefined,
  owner: undefined,
  dateTimeRange: undefined,
  status: undefined,

})

function applyFilters() {
  emit('filter', filters.value)
}
</script>

<template>
  <div class="filters">
    <h2>Filters</h2>
    <form @submit.prevent="applyFilters">
      <input v-model="filters.name" placeholder="Tournament Name">
      <input v-model="filters.owner" placeholder="Owner">
      <n-date-picker v-model="filters.dateTimeRange" type="datetimerange" clearable />
      <pre>{{ JSON.stringify(filters.dateTimeRange) }}</pre>
      <select v-model="filters.status">
        <option :value="STATUS.SCHEDULED">
          Open
        </option>
        <option :value="STATUS.ONGOING">
          On-going
        </option>
        <option :value="STATUS.FINISHED">
          Closed
        </option>
      </select>
      <!-- More filters can be added here -->
      <button type="submit">
        Apply Filters
      </button>
    </form>
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
