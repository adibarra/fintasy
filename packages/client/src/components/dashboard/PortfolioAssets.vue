<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the assets of the user's portfolio.
-->

<script setup lang="ts">
interface Asset {
  symbol: string
  quantity: string
  pl_day: string
  pl_total: string
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
  { key: 'symbol', title: 'Symbol', width: '75px' },
  { key: 'quantity', title: 'Qty', width: '70px' },
  { key: 'pl_day', title: 'P/L Day', width: '85px' },
  { key: 'pl_total', title: 'P/L Total' },
]

const data = ref()
const loading = ref(false)
const pagination = ref({
  page: 1,
  pageCount: Math.ceil(props.assets.length / 7),
  itemsPerPage: 7,
})

function handlePageChange(page: number) {
  pagination.value.page = page
  if (!loading.value) {
    loading.value = true
    setTimeout(() => {
      data.value = props.assets.slice((page - 1) * pagination.value.itemsPerPage, page * pagination.value.itemsPerPage)
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
    remote flex-height
    mt-2 min-h-65 grow
    @update:page="handlePageChange"
  />
</template>