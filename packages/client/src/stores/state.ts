/**
 * @author: adibarra (Alec Ibarra)
 * @description: Pinia store for handling app state
 */

import { acceptHMRUpdate, defineStore } from 'pinia'
import type { Portfolio, Transaction } from '~/types'

const fintasy = useAPI()

export const useStateStore = defineStore('state', () => {
  const user = useStorage<{
    uuid: string
    username: string
    coins: number
  }>('state-user', {
    uuid: '',
    username: '',
    coins: 0,
  })
  const portfolio = ref<{
    active: number
    available: Portfolio[]
  }>({
    active: 0,
    available: [],
  })
  const transactions = ref<Transaction[]>([])

  return {
    user,
    portfolio,
    transactions,
    refresh: {
      user: async () => {
        const userRequest = await fintasy.getUser({ uuid: user.value.uuid })
        if (userRequest.code !== 200)
          return

        user.value.username = userRequest.data.username
        user.value.coins = userRequest.data.coins
      },
      portfolio: async () => {
        const portfoliosRequest = await fintasy.getPortfolios({ owner: user.value.uuid, limit: 99 })
        if (portfoliosRequest.code !== 200)
          return

        portfolio.value.active = 0
        portfolio.value.available = portfoliosRequest.data

        if (portfoliosRequest.data.length !== 0)
          return

        const createPortfolioRequest = await fintasy.createPortfolio({ name: 'Default Portfolio' })
        if (createPortfolioRequest.code !== 200)
          return

        portfolio.value.available = [createPortfolioRequest.data]
      },
      transactions: async () => {
        const transactionsRequest = await fintasy.getTransactions({ portfolio: portfolio.value.available[portfolio.value.active].uuid, limit: 999 })
        if (transactionsRequest.code !== 200)
          return

        transactions.value = transactionsRequest.data
      },
    },
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useStateStore as any, import.meta.hot))
