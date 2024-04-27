<!--
  @author: adibarra (Alec Ibarra), Mariptime (Akshay)
  @description: This component is used to display the login/register page of the application.
-->
<script setup lang="ts">
const { t } = useI18n()
const router = useRouter()
const state = useStateStore()
const fintasy = useAPI()

const activeForm = useStorage<'login' | 'register'>('login-last-form', 'register')
const rememberMe = useStorage('login-remember-me', false)
const username = useStorage('login-username', '')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const waitForLogin = ref(false)

useHead({
  title: `${t('pages.login.title')} • Fintasy`,
})

// make sure uuid is set before redirecting
watch(() => [fintasy.authenticated.value, waitForLogin.value], () => {
  if (fintasy.authenticated.value && !waitForLogin.value)
    router.push('/dashboard')
}, { immediate: true })

async function handleSubmit() {
  if (activeForm.value === 'login')
    await login()
  else
    await createAccount()
}

async function createAccount() {
  if (!email.value || !username.value || !password.value || password.value !== confirmPassword.value) {
    error.value = t('pages.login.missing-credentials')
    return
  }

  const createUser = await fintasy.createUser({ email: email.value, username: username.value, password: password.value })
  switch (createUser.code) {
    case 400:
      error.value = t('pages.login.invalid-registration')
      break
    case 409:
      error.value = t('pages.login.unique-taken')
      break
    case 200:
      login()
      break
    default:
      error.value = t('pages.login.unknown-error')
      break
  }
}

async function login() {
  if (!username.value || !password.value) {
    error.value = t('pages.login.missing-credentials')
    return
  }

  waitForLogin.value = true
  const login = await fintasy.login({ username: username.value, password: password.value })
  switch (login.code) {
    case 404:
      error.value = t('pages.login.no-account-found')
      break
    case 403:
      error.value = t('pages.login.invalid-credentials')
      break
    case 200:
      if (!rememberMe.value)
        username.value = ''
      state.user.uuid = login.data.owner
      break
    default:
      error.value = t('pages.login.unknown-error')
      break
  }
  waitForLogin.value = false
}

function toggleForm() {
  activeForm.value = activeForm.value === 'login' ? 'register' : 'login'

  // clear confirm password if switching forms
  if (activeForm.value === 'register')
    confirmPassword.value = ''
}
</script>

<template>
  <div h-15svh />

  <!-- Login and Registration Forms -->
  <div flex flex-col justify-center>
    <!-- Form Container -->
    <div mx-auto mb-5 max-w-150 min-w-80 w-90svw flex flex-col gap-5 fn-outline bg--c-fg px-8 py-8>
      <!-- Form Title -->
      <div mb-5 text-center text-3xl>
        {{ activeForm === 'login' ? t('pages.login.login') : t('pages.login.register') }}
      </div>

      <!-- Email Input (Only for Registration) -->
      <div v-if="activeForm === 'register'">
        <div fn-outline fn-hover>
          <n-input-group>
            <n-input-group-label class="w-17%" min-w-fit>
              {{ t('pages.login.email') }}
            </n-input-group-label>
            <n-input
              v-model:value="email"
              :placeholder="t('pages.login.email')"
              autocomplete="email"
              type="text"
            />
          </n-input-group>
        </div>
      </div>

      <!-- Username Input -->
      <div>
        <div fn-outline fn-hover>
          <n-input-group>
            <n-input-group-label class="w-17%" min-w-fit>
              {{ t('pages.login.username') }}
            </n-input-group-label>
            <n-input
              v-model:value="username"
              :placeholder="t('pages.login.username')"
              :status="username.length >= 3 || username.length === 0 ? undefined : 'error'"
              :maxlength="20"
              autocomplete="username"
              type="text"
            />
          </n-input-group>
        </div>

        <!-- Username Requirements (Only for Registration) -->
        <div v-if="activeForm === 'register'">
          <div px-2 py-1 op-75>
            {{ t('pages.login.username-requirements') }}
          </div>
        </div>
      </div>

      <!-- Password Input -->
      <div fn-outline fn-hover>
        <n-input-group>
          <n-input-group-label class="w-17%" min-w-fit>
            {{ t('pages.login.password') }}
          </n-input-group-label>
          <n-input
            v-model:value="password"
            :placeholder="t('pages.login.password')"
            :status="password.length >= 6 || password.length === 0 ? undefined : 'error'"
            :autocomplete="activeForm === 'register' ? 'new-password' : 'current-password'"
            type="password"
            show-password-on="click"
            @keypress.enter="handleSubmit"
          />
        </n-input-group>
      </div>

      <!-- Confirm Password Input (Only for Registration) -->
      <div
        v-if="activeForm === 'register'"
        mb-3
      >
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
              @keypress.enter="handleSubmit"
            />
          </n-input-group>
        </div>
        <div px-2 py-1 op-75>
          {{ t('pages.login.password-requirements') }}
        </div>
      </div>

      <!-- Remember and Forgot password (Only for Login) -->
      <div
        v-if="activeForm === 'login'"
        flex items-center justify-between
      >
        <n-checkbox v-model:checked="rememberMe">
          {{ t('pages.login.remember-me') }}
        </n-checkbox>
        <!-- forgot password link commented out for now
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
      <button
        mt-5 fn-outline bg--c-inverse hover:bg--c-accent px-2 py-0.5 text-lg text--c-bg
        @click="handleSubmit"
      >
        {{ activeForm === 'login' ? t('pages.login.sign-in') : t('pages.login.create-account') }}
      </button>

      <!-- Redirect Link -->
      <span flex flex-row items-center justify-center gap-2 text-lg>
        {{ activeForm === 'login' ? t('pages.login.no-account') : t('pages.login.already-have-account') }}
        <a
          cursor-pointer fn-link
          @click="toggleForm"
        >
          {{ activeForm === 'login' ? t('pages.login.sign-up') : t('pages.login.sign-in') }}
        </a>
      </span>
    </div>
  </div>
</template>

<style>
.n-input .n-input__state-border {
  display: none !important;
}
</style>

<route lang="yaml">
  meta:
    layout: home
</route>
