/**
 * @author: adibarra (Alec Ibarra)
 * @description: Pinia store for handling sidebar state
 */

import { acceptHMRUpdate, defineStore } from 'pinia'

export const useSidebarStore = defineStore('sidebar', () => {
  const collapsed = useStorage('sidebar-collapsed', false)
  const toggle = useToggle(collapsed)

  return { collapsed, toggle }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useSidebarStore as any, import.meta.hot))
