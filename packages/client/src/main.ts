/**
 * @author: adibarra (Alec Ibarra)
 * @description: Main entry point for the application
 */

import { setupLayouts } from 'virtual:generated-layouts'
import { createRouter, createWebHistory } from 'vue-router'

import { createHead } from '@unhead/vue'
import { routes } from 'vue-router/auto-routes'
import App from './App.vue'
import type { UserModule } from './types'

import '@unocss/reset/tailwind.css'
import 'uno.css'

const head = createHead()

// create the router instance
const router = createRouter({
  history: createWebHistory(),
  routes: setupLayouts(routes),
})

// Create the Vue app instance
const app = createApp(App)

// install all modules under `modules/`
Object.values(import.meta.glob<{ install: UserModule }>('./modules/*.ts', { eager: true }))
  .forEach(i => i.install?.({ app, router }))

// mount the app
app.use(router)
app.use(head)
app.mount('#app')
