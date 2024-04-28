<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the user's transaction history.
-->

<script setup lang="ts">
import { ACTION, type Transaction } from '~/types'

const props = defineProps({
  name: {
    type: String,
    required: true,
  },
  transactions: {
    type: Array as PropType<Transaction[]>,
    required: true,
  },
})

const { t } = useI18n()

const columns = computed(() => [
  { key: 'symbol', title: t('pages.dashboard.symbol'), width: '20%' },
  { key: 'action', title: t('pages.dashboard.buy-sell-action'), width: '20%' },
  { key: 'quantity', title: t('pages.dashboard.quantity'), width: '15%' },
  { key: 'price_cents', title: t('pages.dashboard.price'), width: '20%' },
  { key: 'created_at', title: t('pages.dashboard.date') },
])

const data = ref<any[]>([])
const loading = computed(() => props.transactions.length === 0)
const pagination = ref({
  page: 1,
  pageSlot: 6,
  itemsPerPage: 14,
  itemCount: computed(() => props.transactions.length),
})

function handlePageChange() {
  const page = pagination.value.page
  const itemsPerPage = pagination.value.itemsPerPage
  data.value = props.transactions
    .slice((page - 1) * itemsPerPage, page * itemsPerPage)
    .map((transaction: Transaction) => {
      return {
        symbol: transaction.symbol,
        action: ACTION[transaction.action],
        quantity: `x${transaction.quantity}`,
        price_cents: `$${(transaction.price_cents / 100).toFixed(2)}`,
        created_at: transaction.created_at,
      }
    })
}

watch(() => [props.transactions, pagination.value.page], () => {
  handlePageChange()
}, { immediate: true })
</script>

<template>
  <div flex>
    <span ml-1 text-xl font-600>
      {{ props.name }}
    </span>
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
      {{ t('pages.dashboard.transactions') }}
    </span>
  </div>
  <!-- eslint-disable unocss/order-attributify -->
  <n-data-table
    :columns="columns"
    :data="data"
    :loading="loading"
    :pagination="pagination"
    :remote="true"
    :flex-height="true"
    mt-2 min-h-65 grow text-xxs sm:text-xs md:text-sm xl:w-110
    @update:page="page => pagination.page = page"
  />
  <!-- eslint-disable unocss/order-attributify -->
</template>
