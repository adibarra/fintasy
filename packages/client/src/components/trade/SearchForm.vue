<script setup lang="ts">
const emit = defineEmits(['search'])

function search(e) {
  emit('search', e.target.value)
}
</script>

<template>
  <form class="w-full flex items-center px-4 py-3">
    <input
      type="text"
      placeholder="Search"
      class="bg-gray-50 pl-2 text-gray-900"
      grow
      fn-outline @input="search"
    >
  </form>
</template>
