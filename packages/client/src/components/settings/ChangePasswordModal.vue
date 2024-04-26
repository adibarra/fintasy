<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the change password modal.
-->

<script setup lang="ts">
const isOpen = defineModel<boolean>()

const { t } = useI18n()
const fintasy = useAPI()
const state = useStateStore()

const password = ref('')
const confirmPassword = ref('')
const error = ref('')

async function changePassword(slotCloseFunc: Function) {
  if (!password.value || !confirmPassword.value) {
    error.value = 'All fields are required'
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  // change password
  const response = await fintasy.updateUser({ uuid: state.user.uuid, password: password.value })
  switch (response.code) {
    case 400:
      error.value = 'Password does not meet requirements'
      return
    case 200:
      break
    default:
      error.value = 'An unknown error occurred. Please try again later.'
      return
  }

  state.refresh.user()
  close(slotCloseFunc)
}

function close(slotCloseFunc: Function) {
  password.value = ''
  error.value = ''
  isOpen.value = false
  slotCloseFunc()
}
</script>

<template>
  <Modal v-model="isOpen">
    <template #header>
      <span ml-2 text-3xl>Change Password</span>
    </template>
    <template #content>
      <div mx-auto max-w-100 min-w-50 w-80svw flex flex-col gap-5 px-8 py-8>
        <div fn-outline fn-hover>
          <n-input-group>
            <n-input-group-label class="w-17%" min-w-fit>
              {{ t('pages.login.password') }}
            </n-input-group-label>
            <n-input
              v-model:value="password"
              placeholder="New Password"
              :status="password.length >= 6 || password.length === 0 ? undefined : 'error'"
              autocomplete="new-password"
              type="password"
              show-password-on="click"
            />
          </n-input-group>
        </div>
        <div>
          <div fn-outline fn-hover>
            <n-input-group>
              <n-input-group-label class="w-17%" min-w-fit>
                {{ t('pages.login.confirm') }}
              </n-input-group-label>
              <n-input
                v-model:value="confirmPassword"
                :placeholder="t('pages.login.confirm-password')"
                :status="password === confirmPassword ? 'success' : 'error'"
                autocomplete="new-password"
                type="password"
                show-password-on="click"
              />
            </n-input-group>
          </div>
          <div px-2 py-1 op-75>
            {{ t('pages.login.password-requirements') }}
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
          @click="changePassword(footerProps.close)"
        >
          <span mx-2>Save</span>
        </button>
      </div>
    </template>
  </Modal>
</template>
