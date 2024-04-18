<script lang="ts">
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'TournamentFilters',
  emits: ['filter'],
  setup(props, { emit }) {
    const range = ref([new Date(), new Date(Date.now() + 86400000)]) // This initializes the range to today and tomorrow.
    const filters = ref({
      name: '',
      owner: '',
      dateTimeRange: range.value,
      status: '',

    })

    const applyFilters = () => {
      emit('filter', filters.value)
    }

    return {
      filters,
      applyFilters,
    }
  },
})
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
        <option value="all">
          All Status
        </option>
        <option value="open">
          Open
        </option>
        <option value="closed">
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
