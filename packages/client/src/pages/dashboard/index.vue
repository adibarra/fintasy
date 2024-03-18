<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: `${t('pages.dashboard.title')} • Fintasy`,
})

const assets = [
  { id: '1', name: 'Apple Inc.' },
  { id: '2', name: 'Microsoft Corporation' },
  { id: '3', name: 'Amazon.com, Inc.' },
]

const transactions = [
  { id: '1', date: '2022-10-01', description: 'Bought 10 shares of Apple Inc.' },
  { id: '2', date: '2022-10-02', description: 'Sold 5 shares of Microsoft Corporation' },
  { id: '3', date: '2022-10-03', description: 'Bought 20 shares of Amazon.com, Inc.' },
]
</script>

<template>
  <div id="widget area" h-full w-full flex flex-col gap-1 lg:flex-row>
    <div id="left area" flex grow flex-col gap-1 lg:w-50vw xl:w-60vw>
      <div flex flex-col fn-outline bg--c-bg-secondary p-2>
        <span text-xl>Portfolio Value</span>
        <div h-85>
          <AMChart />
        </div>
      </div>
      <div flex grow flex-col fn-outline bg--c-bg-secondary p-2>
        <span text-xl>My Assets</span>
        <div grow>
          <ul>
            <li v-for="asset in assets" :key="asset.id">
              {{ asset.name }}
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div id="right area" h-full flex grow flex-row gap-1>
      <div flex grow flex-col fn-outline bg--c-bg-secondary p-2>
        <span text-xl>History</span>
        <div grow>
          <ul>
            <li v-for="transaction in transactions" :key="transaction.id">
              {{ transaction.date }} - {{ transaction.description }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
