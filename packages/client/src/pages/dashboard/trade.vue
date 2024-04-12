<script setup>
// import {onMounted} from "vue";
import DataTable from '~/components/dashboard/DataTable.vue'

// const items = ref([]);
// onMounted(async () => {
//   const response = await fetch()

// })

const items = [
  {
    id: 2,
    price: 250,

  },
  {
    id: 3,
    price: 500,
  },
  {
    id: 4,
    price: 750,
  },
]
</script>

<template>
  <div class="p-8">
    <DataTable :items="items" />
  </div>
</template>
