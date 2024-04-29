<!--
  @author: Zedfoura (Tinatsei Chingaya)
  @description: This component is used to display the filters for the tournaments page of the application.
-->

<script setup lang="ts">
import { STATUS } from '~/types'

interface TournamentFilter {
  owner?: string
  name?: string
  status?: STATUS
  start_date?: Date
  end_date?: Date
}

const emit = defineEmits(['filter'])
const dateTimeRange = ref<[Date?, Date?]>([undefined, undefined])
const filters = ref<TournamentFilter>({
  name: undefined,
  owner: undefined,
  status: undefined,
  start_date: dateTimeRange.value[0],
  end_date: dateTimeRange.value[1],
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

      <!-- might need to use event instead of v-model to properly extract data we need -->
      <n-date-picker v-model="dateTimeRange" type="datetimerange" clearable />

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
      <!-- More filters can be added here -->
      <button
        fn-outline px-2 py-1 fn-hover
        type="submit"
      >
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
