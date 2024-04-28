<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the change email modal.
-->

<script setup lang="ts">
import { useMessage } from 'naive-ui'

const isOpen = defineModel<boolean>()

const { t } = useI18n()
const fintasy = useAPI()
const state = useStateStore()
const message = useMessage()

const email = ref('')
const error = ref('')

async function changeEmail(slotCloseFunc: Function) {
  if (!email.value) {
    error.value = 'Email is required'
    return
  }

  // change email
  const response = await fintasy.updateUser({ uuid: state.user.uuid, email: email.value })
  switch (response.code) {
    case 400:
      error.value = 'Email does not meet requirements'
      return
    case 409:
      error.value = 'Email is already taken'
      return
    case 200:
      break
    default:
      error.value = 'An unknown error occurred. Please try again later.'
      return
  }

  message.info('Email changed successfully')
  state.refresh.user()
  close(slotCloseFunc)
}

function close(slotCloseFunc: Function) {
  email.value = ''
  error.value = ''
  isOpen.value = false
  slotCloseFunc()
}
</script>

<template>
  <Modal v-model="isOpen">
    <template #header>
      <span ml-2 text-3xl>Change Email</span>
    </template>
    <template #content>
      <div mx-auto max-w-100 min-w-50 w-80svw flex flex-col gap-5 px-8 py-8>
        <div>
          <div fn-outline fn-hover>
            <n-input-group>
              <n-input-group-label class="w-17%" min-w-fit>
                {{ t('pages.login.email') }}
              </n-input-group-label>
              <n-input
                v-model:value="email"
                placeholder="newEmail@example.com"
                autocomplete="none"
                type="text"
              />
            </n-input-group>
          </div>
        </div>
        <div v-if="error" px-2 py-1 text-red>
          {{ error }}
        </div>
      </div>
    </template>
    <template #footer="footerProps">
      <div flex gap-2 flex-justify-end>
        <button
          fn-outline p-1 px-2 fn-hover
          @click="close(footerProps.close)"
        >
          <span mx-2>Cancel</span>
        </button>
        <button
          fn-outline bg--c-inverse p-1 px-2 text--c-bg
          @click="changeEmail(footerProps.close)"
        >
          <span mx-2>Save</span>
        </button>
      </div>
    </template>
  </Modal>
</template>
