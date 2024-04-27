<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the assets of the user's portfolio.
-->

<script setup lang="ts">
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

const { t } = useI18n()

interface Asset {
  symbol: string
  quantity: number
  price_cents: number
  pl_day: number
  pl_total: number
}

const columns = computed(() => [
  { key: 'symbol', title: t('pages.dashboard.symbol'), width: '20%' },
  { key: 'quantity', title: t('pages.dashboard.quantity'), width: '15%' },
  { key: 'price_cents', title: t('pages.dashboard.price'), width: '20%' },
  { key: 'pl_day', title: t('pages.dashboard.profit-loss-day') },
  { key: 'pl_total', title: t('pages.dashboard.profit-loss-total') },
])

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
    <span ml-1 text-xl font-600>
      {{ t('pages.dashboard.assets') }}
    </span>
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
      {{ t('pages.dashboard.cash') }}
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
    mt-2 min-h-65 grow text-xxs sm:text-xs md:text-sm
    @update:page="handlePageChange"
  />
  <!-- eslint-enable unocss/order-attributify -->
</template>
