<script setup>
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
  <!-- main wrapper div -->
  <div flex grow gap-3>
    <div h-full w-25vw bg--c-fg>
      left div
      <div p-8>
        <DataTable :items="items" />
      </div>
    </div>

    <div grow bg--c-fg>
      right div
    </div>
  </div>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
