<!--
  @author: adibarra (Alec Ibarra), maclark (Mason Clark)
  @description: This component is used to display rows in the data table in the trading page.
-->

<script setup lang="ts">
import { ACTION, type Quote } from '~/types'

const props = defineProps({
  assetMap: {
    type: Object as PropType<Record<string, number>>,
    required: true,
  },
  quote: {
    type: Object as PropType<Quote>,
    required: true,
  },
})

const state = useStateStore()
const fintasy = useAPI()

const quantity = ref(0)

async function createTransaction(action: ACTION) {
  const uuid = state.portfolio.available[state.portfolio.active].uuid
  await fintasy.createTransaction({
    portfolio: uuid,
    symbol: props.quote.symbol,
    action,
    quantity: quantity.value,
  })
  await state.refresh.portfolios()
}
</script>

<template>
  <td class="px-2 py-2" w-15 grow text-center>
    {{ quote.symbol }}
  </td>
  <td class="px-2 py-2" w-11 grow text-center>
    {{ `$${(quote.price_cents / 100).toFixed(2)}` }}
  </td>
  <td class="px-2 py-2" w-11 grow text-center>
    <input
      v-model="quantity"
      type="number"
      min="0"
      max="100"
      placeholder="Qty"
      w-15 fn-outline bg--c-fg text-center text--c-inverse
      @input="quantity = Math.abs(quantity)"
    >
  </td>
  <td w-15 flex grow justify-center gap-2 p-1>
    <button
      b-1 bg-lime-600 px-2 py-1 dark:bg-lime-500 hover:bg-lime-700 hover:dark:bg-lime-600
      @click="createTransaction(ACTION.BUY)"
    >
      ✓
    </button>
    <button
      b-1 bg-red-500 px-2 py-1 hover:bg-red-600
      @click="createTransaction(ACTION.SELL)"
    >
      ✕
    </button>
  </td><td class="px-2 py-2" w-15 grow text-center>
    {{ props.assetMap[quote.symbol] || 0 }}
  </td>
</template>
