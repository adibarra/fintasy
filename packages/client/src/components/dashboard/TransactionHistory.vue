<script setup lang="ts">
import { ACTION, type Transaction } from '~/types'

const props = defineProps({
  transactions: {
    type: Array as PropType<Transaction[]>,
    required: true,
  },
})

const columns = [
  { key: 'symbol', title: 'Symbol', width: '75px' },
  { key: 'action', title: 'Action', width: '70px' },
  { key: 'quantity', title: 'Qty', width: '70px' },
  { key: 'price_cents', title: 'Price' },
  { key: 'created_at', title: 'Date' },
]

const data = ref()
const loading = ref(false)
const pagination = ref({
  page: 1,
  pageCount: Math.ceil(props.transactions.length / 14),
  itemsPerPage: 14,
})

function handlePageChange(page: number) {
  pagination.value.page = page
  if (!loading.value) {
    loading.value = true
    setTimeout(() => {
      data.value = props.transactions.slice((page - 1) * pagination.value.itemsPerPage, page * pagination.value.itemsPerPage)
      data.value = data.value.map((transaction: Transaction) => {
        return {
          symbol: transaction.symbol,
          action: ACTION[transaction.action],
          quantity: `x${transaction.quantity}`,
          price_cents: `$${(transaction.price_cents / 100).toFixed(2)}`,
          created_at: transaction.created_at,
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
    mt-2 min-h-65 grow xl:w-110
    @update:page="handlePageChange"
  />
</template>
