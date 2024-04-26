<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the settings page of the application.
-->

<script setup lang="ts">
const { t } = useI18n()

const emailModal = ref(false)
const usernameModal = ref(false)
const passwordModal = ref(false)
const deleteModal = ref(false)

useHead({
  title: `${t('pages.dashboard.settings.title')} • Fintasy`,
})
</script>

<template>
  <div h-full w-full flex flex-col gap-2 xl:flex-row>
    <div flex grow flex-col fn-outline bg--c-fg p-2 max-xl:h-205>
      <div mb-4 ml-2 text-3xl>
        {{ t('pages.dashboard.settings.title') }}
      </div>
      <div max-w-100 min-w-60 w-50svw flex grow flex-col gap-5 px-4 pb-4>
        <button
          fn-outline px-2 py-0.5 text-lg
          @click="emailModal = true"
        >
          Change Email
        </button>
        <button
          fn-outline px-2 py-0.5 text-lg
          @click="usernameModal = true"
        >
          Change Username
        </button>
        <button
          fn-outline px-2 py-0.5 text-lg
          @click="passwordModal = true"
        >
          Change Password
        </button>
        <div grow />
        <button
          fn-outline px-2 py-0.5 text-lg text-red
          @click="deleteModal = true"
        >
          Delete Account
        </button>
      </div>
    </div>
  </div>
  <ChangeEmailModal v-model="emailModal" />
  <ChangeUsernameModal v-model="usernameModal" />
  <ChangePasswordModal v-model="passwordModal" />
  <DeleteUserModal v-model="deleteModal" />
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
