<script>
export default {
  props: {
    visible: Boolean,
    tournament: {
      type: Object,
      default: () => ({}),
    },
  },
  methods: {
    closeModal() {
      this.$emit('close')
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString('en-US') // Adjust format as necessary
    },
  },
}
</script>

<template>
  <div v-if="visible" class="modal">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h2>{{ tournament.name }}</h2>
      <p><strong>Owner:</strong> {{ tournament.owner }}</p>
      <p><strong>Status:</strong> {{ tournament.status }}</p>
      <p><strong>Start Date:</strong> {{ formatDate(tournament.start_date) }}</p>
      <p><strong>End Date:</strong> {{ formatDate(tournament.end_date) }}</p>
      <p><strong>Created At:</strong> {{ formatDate(tournament.created_at) }}</p>
      <p><strong>Updated At:</strong> {{ formatDate(tournament.updated_at) }}</p>
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
