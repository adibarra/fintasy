<script setup lang="ts">
interface Transaction {
  uuid: string
  portfolio: string
  symbol: string
  action: string
  quantity: string
  price_cents: string
  created_at: string
}

const props = defineProps({
  transactions: {
    type: Array as PropType<Transaction[]>,
    required: true,
  },
})

const columns = [
  {
    key: 'symbol',
    title: 'Symbol',
  },
  {
    key: 'action',
    title: 'Action',
  },
  {
    key: 'quantity',
    title: 'Qty',
  },
  {
    key: 'price_cents',
    title: 'Price',
  },
  {
    key: 'created_at',
    title: 'Date',
  },
]

const data = ref()
const pagination = ref({
  page: 1,
  pageCount: Math.ceil(props.transactions.length / 10),
  itemsPerPage: 10,
})
const loading = ref<boolean>(false)
function handlePageChange(page: number) {
  pagination.value.page = page
  if (!loading.value) {
    loading.value = true
    setTimeout(() => {
      data.value = props.transactions.slice((page - 1) * pagination.value.itemsPerPage, page * pagination.value.itemsPerPage)
      loading.value = false
    }, 250)
  }
}

onMounted(() => handlePageChange(1))
</script>

<template>
  <div flex>
    <span ml-1 text-xl font-600>History</span>
    <div grow />
    <span mx-2 text-xl>
      <n-number-animation
        :from="0"
        :to="transactions.length"
        :duration="4000"
        :active="true"
        show-separator
      />
    </span>
    <span mr-2 mt-auto op-75>
      TRANSACTIONS
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
