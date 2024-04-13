<script setup>
// const items = ref([]);
// onMounted(async () => {
//   const response = await fetch()

// })
const trend = generateData(Math.floor(Math.random() * 1500) + 500)

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

function generateData(count) {
  const data = []
  const startDate = new Date().getTime() - 1000 * 60 * 15 * count
  let value = 1000

  for (let i = 0; i < count; ++i) {
    value = Math.round((Math.random() * 1 - 0.495) * 100 + value)
    data.push({
      date: startDate + 1000 * 60 * 15 * i,
      value,
    })
  }
  return data
}
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

    <div grow p-10>
      <div h-80>
        <PortfolioChart :data="trend" />
      </div>
    </div>
  </div>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
