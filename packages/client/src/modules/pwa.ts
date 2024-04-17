/**
 * @author: adibarra (Alec Ibarra)
 * @description: Usermodule for installing vite-plugin-pwa
 */

import type { UserModule } from '~/types'

// https://github.com/antfu/vite-plugin-pwa#automatic-reload-when-new-content-available
export const install: UserModule = ({ router }) => {
  router.isReady()
    .then(async () => {
      const { registerSW } = await import('virtual:pwa-register')
      registerSW({ immediate: true })
    })
    .catch(() => {})
}
