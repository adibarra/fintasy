<script setup>
const emit = defineEmits(['search'])

function search(e) {
  emit('search', e.target.value)
};
</script>

<template>
  <form class="flex items-center px-4 py-3">
    <label class="sr-only">Search</label>

    <div class="relative w-full">
      <input type="text" placeholder="Search" class="border border-white rounded-lg bg-gray-50 pl-2 text-gray-900" @input="search">
    </div>
  </form>
</template>
