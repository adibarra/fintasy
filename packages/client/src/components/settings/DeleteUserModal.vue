<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the delete user modal.
-->

<script setup lang="ts">
import { useMessage } from 'naive-ui'

const isOpen = defineModel<boolean>()

const fintasy = useAPI()
const state = useStateStore()
const message = useMessage()

const error = ref('')

async function deleteUser(slotCloseFunc: Function) {
  // delete user
  const response = await fintasy.deleteUser({ uuid: state.user.uuid })
  switch (response.code) {
    case 200:
      break
    default:
      error.value = 'An unknown error occurred. Please try again later.'
      return
  }

  message.success('User deleted successfully')
  state.refresh.user()
  close(slotCloseFunc)
}

function close(slotCloseFunc: Function) {
  error.value = ''
  isOpen.value = false
  slotCloseFunc()
}
</script>

<template>
  <Modal v-model="isOpen">
    <template #header>
      <span ml-2 text-3xl>Delete User</span>
    </template>
    <template #content>
      <div mx-auto max-w-100 min-w-50 w-80svw flex flex-col gap-5 px-8 py-8>
        You are about to delete your account. This action is irreversible.
        Are you sure you want to proceed?
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
          fn-outline bg-red p-1 px-2 text--c-bg
          @click="deleteUser(footerProps.close)"
        >
          <span mx-2>Delete</span>
        </button>
      </div>
    </template>
  </Modal>
</template>
