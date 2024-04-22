/**
 * @author: adibarra (Alec Ibarra)
 * @description: Pinia store for handling app state
 */

import { acceptHMRUpdate, defineStore } from 'pinia'
import type { Portfolio } from '~/types'

export const useStateStore = defineStore('state', () => {
  const user = useStorage('state-user', {
    uuid: '',
    username: '',
    coins: 0,
  })
  const portfolio = ref({
    active: 0,
    available: [] as Portfolio[],
  })

  return { user, portfolio }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useStateStore as any, import.meta.hot))
