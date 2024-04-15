/**
 * @author: adibarra (Alec Ibarra)
 * @description: Pinia store for handling app state
 */

import { acceptHMRUpdate, defineStore } from 'pinia'
import type { Portfolio } from '~/types'

export const useStateStore = defineStore('state', () => {
  const auth = ref({
    authenticated: false,
    uuid: '',
  })
  const user = ref({
    username: '',
    avatar: 'https://avatars.githubusercontent.com/u/93070681?v=4',
    coins: 0,
  })
  const portfolio = ref({
    active: 0,
    available: [] as Portfolio[],
  })

  return { auth, user, portfolio }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useStateStore as any, import.meta.hot))
