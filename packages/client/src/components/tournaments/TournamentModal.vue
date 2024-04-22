<script setup lang="ts">
import type { Tournament } from '~/types'

const props = defineProps({
  visible: {
    type: Boolean,
    required: true,
  },
  tournament: {
    type: Object as PropType<Tournament>,
    required: true,
  },
})

const emit = defineEmits(['close'])

function closeModal() {
  emit('close')
}

function formatDate(date: string) {
  // Adjust format as necessary
  return new Date(date).toLocaleDateString('en-US')
}
</script>

<template>
  <div v-if="props.visible" class="modal">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h2>{{ props.tournament.name }}</h2>
      <p><strong>Owner:</strong> {{ props.tournament.owner }}</p>
      <p><strong>Status:</strong> {{ props.tournament.status }}</p>
      <p><strong>Start Date:</strong> {{ formatDate(props.tournament.start_date) }}</p>
      <p><strong>End Date:</strong> {{ formatDate(props.tournament.end_date) }}</p>
      <p><strong>Created At:</strong> {{ formatDate(props.tournament.created_at) }}</p>
      <p><strong>Updated At:</strong> {{ formatDate(props.tournament.updated_at) }}</p>
    </div>
  </div>
</template>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: black;
  padding: 20px;
  border-radius: 5px;
  width: 90%;
  max-width: 500px;
}
.close {
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
  font-size: 1.5em;
}
</style>
