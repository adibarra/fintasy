<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the add portfolio modal.
-->

<script setup lang="ts">
import { useMessage } from 'naive-ui'

const isOpen = defineModel<boolean>()

const fintasy = useAPI()
const state = useStateStore()
const message = useMessage()

const portfolioName = ref('')
const error = ref('')

async function createPortfolio(slotCloseFunc: Function) {
  if (!portfolioName.value) {
    error.value = 'Portfolio name is required'
    return
  }

  // add portfolio
  const response = await fintasy.createPortfolio({ name: portfolioName.value })
  switch (response.code) {
    case 400:
      error.value = 'Portfolio name does not meet requirements'
      return
    case 200:
      break
    default:
      error.value = 'An unknown error occurred. Please try again later.'
      return
  }

  message.info('Portfolio created successfully')
  state.refresh.portfolios()
  close(slotCloseFunc)
}

function close(slotCloseFunc: Function) {
  portfolioName.value = ''
  error.value = ''
  isOpen.value = false
  slotCloseFunc()
}
</script>

<template>
  <Modal v-model="isOpen">
    <template #header>
      <span ml-2 text-3xl>Add Portfolio</span>
    </template>
    <template #content>
      <div mx-auto max-w-100 min-w-50 w-80svw flex flex-col gap-5 px-8 py-8>
        <div>
          <div fn-outline fn-hover>
            <n-input-group>
              <n-input-group-label class="w-17%" min-w-fit>
                Name
              </n-input-group-label>
              <n-input
                v-model:value="portfolioName"
                placeholder="New Portfolio"
                autocomplete="none"
                type="text"
              />
            </n-input-group>
          </div>
          <div v-if="error" px-2 py-1 text-red>
            {{ error }}
          </div>
        </div>
      </div>
    </template>
    <template #footer="footerProps">
      <div flex gap-2 flex-justify-end>
        <button
          fn-outline p-1 px-2 fn-hover
          @click="close(footerProps.close)"
        >
          <span mx-2>Close</span>
        </button>
        <button
          fn-outline bg--c-inverse hover:bg--c-accent p-1 px-2 text--c-bg
          @click="createPortfolio(footerProps.close)"
        >
          <span mx-2>Submit</span>
        </button>
      </div>
    </template>
  </Modal>
</template>
