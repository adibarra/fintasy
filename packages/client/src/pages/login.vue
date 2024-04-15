<!--
  @author: adibarra (Alec Ibarra), Mariptime (Akshay)
  @description: This component is used to display the login/register page of the application.
-->
<script setup lang="ts">
const { t } = useI18n()
const router = useRouter()
const state = useStateStore()
const fintasy = useAPI()

const activeForm = ref<'login' | 'register'>('register')
const rememberMe = useStorage('remember-me', false)
const email = rememberMe.value ? useStorage('email', '') : ref('')
const password = ref('')
const username = ref('')
const confirmPassword = ref('')
const error = ref('')

useHead({
  title: `${t('pages.login.title')} • Fintasy`,
})

async function handleSubmit() {
  if (activeForm.value === 'login')
    await login()
  else
    await createAccount()
}

async function login() {
  if (!email.value || !password.value) {
    error.value = t('pages.login.missing-credentials')
    return
  }

  const status = await fintasy.login({ email: email.value, password: password.value })

  if (status.code === 200) {
    state.auth.authenticated = true
    router.push('/dashboard')
  }
  else {
    error.value = t('pages.login.invalid-credentials')
  }
}

async function createAccount() {
  if (!email.value || !username.value || !password.value || password.value !== confirmPassword.value) {
    error.value = t('pages.login.missing-credentials')
    return
  }

  const status = await fintasy.createUser({ email: email.value, username: username.value, password: password.value })

  if (status.code === 200) {
    state.auth.authenticated = true
    router.push('/dashboard')
  }
  else {
    error.value = t('pages.login.invalid-registration')
  }
}

function toggleForm(form: 'login' | 'register') {
  activeForm.value = form
}
</script>

<template>
  <nav class="mb-8 flex md:mx-6 md:my-4">
    <router-link to="/" class="flex items-center justify-center gap-2">
      <img src="/pwa-192x192.png" alt="Fintasy Logo" class="h-14">
      <div class="text-2xl lg:text-4xl md:text-3xl">
        Fintasy
      </div>
    </router-link>
    <div class="grow" />
    <div class="flex items-center gap-5">
      <button class="rd-10 bg--c-accent hover:bg--c-inverse px-6 py-2 text--c-bg md:text-lg" @click="$router.push('/')">
        {{ t('misc.home') }}
      </button>
    </div>
  </nav>

  <div h-15svh />

  <!-- Login and Registration Forms -->
  <div v-show="activeForm === 'login' || activeForm === 'register'" flex flex-col justify-center>
    <!-- Form Title -->
    <div mb-5 text-center text-3xl>
      {{ activeForm === 'login' ? t('pages.login.title') : t('pages.login.register') }}
    </div>

    <!-- Form Container -->
    <div mx-auto mb-5 max-w-150 min-w-80 w-90vw flex flex-col gap-5 fn-outline px-8 py-8>
      <!-- Email Input -->
      <div fn-outline fn-hover>
        <n-input-group>
          <n-input-group-label>Email</n-input-group-label>
          <n-input
            v-model:value="email" :placeholder="t('pages.login.email')"
            type="text"
          />
        </n-input-group>
      </div>

      <!-- Username Input (Only for Registration) -->
      <div v-if="activeForm === 'register'" mb-5 fn-outline fn-hover>
        <n-input-group>
          <n-input-group-label>Username</n-input-group-label>
          <n-input
            v-model:value="username" :placeholder="t('pages.login.username')"
            type="text"
          />
        </n-input-group>
      </div>

      <!-- Password Input -->
      <div fn-outline fn-hover>
        <n-input-group>
          <n-input-group-label>Password</n-input-group-label>
          <n-input
            v-model:value="password" :placeholder="t('pages.login.password')"
            type="password" show-password-on="click"
            @keypress.enter="handleSubmit"
          />
        </n-input-group>
      </div>

      <!-- Confirm Password Input (Only for Registration) -->
      <div v-if="activeForm === 'register'" fn-outline fn-hover>
        <n-input-group>
          <n-input-group-label>Confirm</n-input-group-label>
          <n-input
            v-model:value="confirmPassword" :placeholder="t('pages.login.confirm-password')"
            type="password" show-password-on="click"
            @keypress.enter="handleSubmit"
          />
        </n-input-group>
      </div>

      <!-- Remember and Forgot password (Only for Login) -->
      <div v-if="activeForm === 'login'" flex items-center justify-between>
        <n-checkbox v-model:checked="rememberMe">
          {{ t('pages.login.remember-me') }}
        </n-checkbox>
        <div grow />

        <!-- Commented out for now -->
        <!--
        <router-link to="/forgot-password" fn-link>
          {{ t('pages.login.forgot-password') }}
        </router-link>
        -->
      </div>

      <!-- Error Message -->
      <div v-if="error" text-red>
        {{ error }}
      </div>

      <!-- Submit Button -->
      <n-button mt-5 text-lg @click="handleSubmit">
        {{ activeForm === 'login' ? t('pages.login.sign-in') : t('pages.login.sign-up') }}
      </n-button>
    </div>

    <!-- Redirect Link -->
    <div
      flex cursor-pointer items-center justify-center fn-link
      @click="toggleForm(activeForm === 'login' ? 'register' : 'login')"
    >
      {{ activeForm === 'login' ? t('pages.login.no-account-create-one') : t('pages.login.already-have-account') }}
    </div>
  </div>
</template>

<route lang="yaml">
  meta:
    layout: default
</route>
