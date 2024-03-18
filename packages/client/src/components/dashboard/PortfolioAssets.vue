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
  pageCount: Math.ceil(props.assets.length / 8),
  itemsPerPage: 8,
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

onMounted(() => handlePageChange(1))
</script>

<template>
  <span ml-1 text-xl>Assets</span>
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
