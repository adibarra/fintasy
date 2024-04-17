/**
 * @author: adibarra (Alec Ibarra)
 * @description: Usermodule for installing pinia
 */

import { createPinia } from 'pinia'
import type { UserModule } from '~/types'

export const install: UserModule = ({ app }) => {
  const pinia = createPinia()
  app.use(pinia)
}
