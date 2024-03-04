<script setup lang="ts">
const { t } = useI18n()
const route = useRoute()

const breadcrumbs = computed(() => {
  const parts = route.path.split('/').filter(Boolean)

  let path = ''
  return parts.map((part: string) => {
    path += `/${part}`
    return {
      label: t(`pages.${path.replaceAll('/', '.').slice(1)}.title`),
      key: path,
    }
  })
})
</script>

<template>
  <n-layout-header bordered h-45px flex items-center>
    <div w-60 />
    <n-breadcrumb>
      <template v-for="crumb in breadcrumbs" :key="crumb">
        <n-breadcrumb-item>
          <router-link :to="crumb.key">
            {{ crumb.label }}
          </router-link>
        </n-breadcrumb-item>
      </template>
    </n-breadcrumb>
    <div />
  </n-layout-header>
</template>
