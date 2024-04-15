/**
 * @author: adibarra (Alec Ibarra)
 * @description: Pinia store for handling app state
 */

import { acceptHMRUpdate, defineStore } from 'pinia'

export const useStateStore = defineStore('state', () => {
  const auth = ref({
    authenticated: false,
  })
  const user = ref({
    username: 'adibarra',
    avatar: 'https://avatars.githubusercontent.com/u/93070681?v=4',
    coins: 15,
  })
  const portfolio = ref({
    active: 'Default Portfolio',
    available: [
      { key: 0, label: 'Default Portfolio' },
      { key: 1, label: 'Test Portfolio' },
      { key: 2, label: 'Tournament Portfolio' },
    ],
  })

  return { auth, user, portfolio }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useStateStore as any, import.meta.hot))
