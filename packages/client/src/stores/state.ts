/**
 * @author: adibarra (Alec Ibarra)
 * @description: Pinia store for handling app state
 */

import { acceptHMRUpdate, defineStore } from 'pinia'
import type { Portfolio, Transaction } from '~/types'

const fintasy = useAPI()

export const useStateStore = defineStore('state', () => {
  interface UserState {
    uuid: string
    username: string
    coins: number
  }

  interface PortfolioState {
    active: number
    available: Portfolio[]
  }

  const user = useStorage<UserState>('state-user', {
    uuid: '',
    username: '',
    coins: 0,
  })
  const portfolio = ref<PortfolioState>({
    active: 0,
    available: [],
  })
  const transactions = ref<Transaction[]>([])

  async function refreshUser() {
    const userRequest = await fintasy.getUser({ uuid: user.value.uuid })
    if (userRequest.code !== 200)
      return

    user.value.username = userRequest.data.username
    user.value.coins = userRequest.data.coins

    await refreshPortfolios()
  }

  async function refreshPortfolios() {
    const portfoliosRequest = await fintasy.getPortfolios({ owner: user.value.uuid, limit: 99 })
    if (portfoliosRequest.code !== 200)
      return

    portfolio.value.active = 0
    portfolio.value.available = portfoliosRequest.data
      .toSorted((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())

    if (portfoliosRequest.data.length !== 0)
      return

    const createPortfolioRequest = await fintasy.createPortfolio({ name: 'Default Portfolio' })
    if (createPortfolioRequest.code !== 200)
      return

    portfolio.value.available = [createPortfolioRequest.data]

    await refreshTransactions()
  }

  async function refreshTransactions() {
    const transactionsRequest = await fintasy.getTransactions({ portfolio: portfolio.value.available[portfolio.value.active].uuid, limit: 999 })
    if (transactionsRequest.code !== 200)
      return

    transactions.value = transactionsRequest.data
      .toSorted((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
  }

  async function refreshAll() {
    await refreshUser()
    await refreshPortfolios()
    await refreshTransactions()
  }

  watch(() => user.value.uuid, refreshAll)
  watch(() => portfolio.value.active, refreshTransactions)

  return {
    user,
    portfolio,
    transactions,
    refresh: {
      all: refreshAll,
      user: refreshUser,
      portfolios: refreshPortfolios,
      transactions: refreshTransactions,
    },
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useStateStore as any, import.meta.hot))
