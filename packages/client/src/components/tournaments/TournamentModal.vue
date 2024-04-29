<!--
  @author: Zedfoura (Tinatsei Chingaya)
  @description: This component is used to display the tournament modal.
-->

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
      <p><strong>Created On:</strong> {{ formatDate(props.tournament.created_at) }}</p>
      <p><strong>Last Updated:</strong> {{ formatDate(props.tournament.updated_at) }}</p>
      <button
        fn-outline px-2 py-1 fn-hover
        @click="closeModal"
      >
        Close
      </button>
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
  z-index: 999;
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
