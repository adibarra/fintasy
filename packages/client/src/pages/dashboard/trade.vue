<script setup>
const fintasy = useAPI()

const trend = generateData(Math.floor(Math.random() * 1500) + 500)
const items = generateAssets(Math.floor(Math.random() * 100) + 100)

// Generate random test data
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

// Generate random assets
function generateAssets(count) {
  const assets = []

  for (let i = 0; i < count; ++i) {
    assets.push({
      symbol: Math.random().toString(36).substring(2, 6).toUpperCase(),
      price_cents: Math.random() * 10000 + 2500,
    })
  }
  return assets
}

onMounted(async () => {
  // const response = await fintasy.get
  // if (Response.code === 200)
  //   items.value = response.data
  // else
  //   console.log('Error fetching data')
})
</script>

<template>
  <!-- main wrapper div -->
  <div flex grow gap-3>
    <!-- left side div -->
    <div h-full w-25vw fn-outline bg--c-fg>
      <div m-8 fn-outline>
        <DataTable :items="items" />
      </div>
    </div>

    <!-- right side div -->
    <div grow fn-outline bg--c-fg p-10>
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
