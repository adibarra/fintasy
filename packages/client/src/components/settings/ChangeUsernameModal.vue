<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the change username modal.
-->

<script setup lang="ts">
import { useMessage } from 'naive-ui'

const isOpen = defineModel<boolean>()

const { t } = useI18n()
const fintasy = useAPI()
const state = useStateStore()
const message = useMessage()

const username = ref('')
const error = ref('')

async function changeUsername(slotCloseFunc: Function) {
  if (!username.value) {
    error.value = 'Username is required'
    return
  }

  // change username
  const response = await fintasy.updateUser({ uuid: state.user.uuid, username: username.value })
  switch (response.code) {
    case 400:
      error.value = 'Username does not meet requirements'
      return
    case 409:
      error.value = 'Username is already taken'
      return
    case 200:
      break
    default:
      error.value = 'An unknown error occurred. Please try again later.'
      return
  }

  message.info('Username changed successfully')
  state.refresh.user()
  close(slotCloseFunc)
}

function close(slotCloseFunc: Function) {
  username.value = ''
  error.value = ''
  isOpen.value = false
  slotCloseFunc()
}
</script>

<template>
  <Modal v-model="isOpen">
    <template #header>
      <span ml-2 text-3xl>Change Username</span>
    </template>
    <template #content>
      <div mx-auto max-w-100 min-w-50 w-80svw flex flex-col gap-5 px-8 py-8>
        <div>
          <div fn-outline fn-hover>
            <n-input-group>
              <n-input-group-label class="w-17%" min-w-fit>
                Username
              </n-input-group-label>
              <n-input
                v-model:value="username"
                placeholder="CoolNewUsername"
                autocomplete="none"
                type="text"
              />
            </n-input-group>
          </div>
          <div px-2 py-1 op-75>
            {{ t('pages.login.username-requirements') }}
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
          @click="changeUsername(footerProps.close)"
        >
          <span mx-2>Save</span>
        </button>
      </div>
    </template>
  </Modal>
</template>
