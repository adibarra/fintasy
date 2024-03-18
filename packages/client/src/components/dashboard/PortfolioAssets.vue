<script setup lang="ts">
interface Asset {
  symbol: string
  quantity: number | string
  pl_day: number | string
  pl_total: number | string
}

const props = defineProps({
  assets: {
    type: Array as PropType<Asset[]>,
    required: true,
  },
})

const columns = [
  {
    key: 'symbol',
    title: 'Symbol',
  },
  {
    key: 'quantity',
    title: 'Qty',
  },
  {
    key: 'pl_day',
    title: 'P/L Day',
  },
  {
    key: 'pl_total',
    title: 'P/L Total',
  },
]

const data = ref()
const pagination = ref({
  page: 1,
  pageCount: Math.ceil(props.assets.length / 10),
  itemsPerPage: 10,
})
const loading = ref<boolean>(false)
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

onMounted(() => {
  props.assets.forEach((asset: Asset) => {
    asset.quantity = `x${asset.quantity}`
    asset.pl_day = `${asset.pl_day}%`
    asset.pl_total = `${asset.pl_total}%`
  })
  handlePageChange(1)
})
</script>

<template>
  <span text-xl>Assets</span>
  <n-data-table
    remote
    :columns="columns"
    :data="data"
    :loading="loading"
    :pagination="pagination"
    flex-height
    mt-2
    grow @update:page="handlePageChange"
  />
</template>
