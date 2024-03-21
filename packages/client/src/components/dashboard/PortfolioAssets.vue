<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the assets of the user's portfolio.
-->

<script setup lang="ts">
interface Asset {
  symbol: string
  quantity: number
  price_cents: number
  pl_day: number
  pl_total: number
}

const props = defineProps({
  assets: {
    type: Array as PropType<Asset[]>,
    required: true,
  },
  cash: {
    type: Number,
    required: true,
  },
})

const columns = [
  { key: 'symbol', title: 'Symbol', width: '20%' },
  { key: 'quantity', title: 'Qty', width: '15%' },
  { key: 'price_cents', title: 'Price', width: '20%' },
  { key: 'pl_day', title: 'P/L Day' },
  { key: 'pl_total', title: 'P/L Total' },
]

const data = ref()
const loading = ref(false)
const pagination = ref({
  page: 1,
  pageSlot: 6,
  itemsPerPage: 7,
  itemCount: props.assets.length,
})

function handlePageChange(page: number) {
  pagination.value.page = page
  if (!loading.value) {
    loading.value = true
    setTimeout(() => {
      data.value = props.assets.slice((page - 1) * pagination.value.itemsPerPage, page * pagination.value.itemsPerPage)
      data.value = data.value.map((asset: Asset) => {
        return {
          symbol: asset.symbol,
          quantity: `x${asset.quantity}`,
          price_cents: `$${(asset.price_cents / 100).toFixed(2)}`,
          pl_day: `$${(asset.pl_day / 100).toFixed(2)}`,
          pl_total: `$${(asset.pl_total / 100).toFixed(2)}`,
        }
      })
      loading.value = false
    }, 250)
  }
}

onMounted(() => handlePageChange(1))
</script>

<template>
  <div flex>
    <span ml-1 text-xl font-600>Assets</span>
    <div grow />
    <span mx-2 text-xl>
      $
      <n-number-animation
        :from="0"
        :to="cash"
        :duration="4000"
        :active="true"
        show-separator
      />
    </span>
    <span mr-2 mt-auto op-75>
      CASH
    </span>
  </div>
  <n-data-table
    :columns="columns"
    :data="data"
    :loading="loading"
    :pagination="pagination"
    :remote="true"
    :flex-height="true"
    mt-2 min-h-65 grow sm:text-xs text-xxs md:text-sm
    @update:page="handlePageChange"
  />
</template>
