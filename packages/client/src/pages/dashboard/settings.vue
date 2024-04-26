<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the settings page of the application.
-->

<script setup lang="ts">
const { t } = useI18n()

const usernameModal = ref(false)
const emailModal = ref(false)
const passwordModal = ref(false)
const deleteModal = ref(false)

useHead({
  title: `${t('pages.dashboard.settings.title')} • Fintasy`,
})
</script>

<template>
  <div h-full w-full flex flex-col gap-2 xl:flex-row>
    <div flex grow flex-col fn-outline bg--c-fg p-2 max-xl:h-205>
      <div mb-5 max-w-150 min-w-80 w-90svw flex flex-col gap-5 px-8 py-8>
        <div flex gap-4>
          Change Language: <LanguageSwitch />
        </div>
        <button
          mt-5 fn-outline px-2 py-0.5 text-lg
          @click="usernameModal = true"
        >
          Change Username
        </button>
        <button
          mt-5 fn-outline px-2 py-0.5 text-lg
          @click="emailModal = true"
        >
          Change Email
        </button>
        <button
          mt-5 fn-outline px-2 py-0.5 text-lg
          @click="passwordModal = true"
        >
          Change Password
        </button>
        <button
          mt-5 fn-outline px-2 py-0.5 text-lg text-red
          @click="deleteModal = true"
        >
          Delete Account
        </button>
      </div>
    </div>
  </div>
  <ChangeUsernameModal v-model="usernameModal" />
  <ChangeEmailModal v-model="emailModal" />
  <ChangePasswordModal v-model="passwordModal" />
  <DeleteUserModal v-model="deleteModal" />
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
