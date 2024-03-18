<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
})

const { t } = useI18n()
useHead({
  title: `${t(props.title)} • Fintasy`,
})
</script>

<template>
  <div />
</template>
