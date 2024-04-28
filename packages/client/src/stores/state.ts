/**
 * @author: adibarra (Alec Ibarra)
 * @description: Pinia store for handling app state
 */

import { acceptHMRUpdate, defineStore } from 'pinia'
import type { Portfolio, Tournament, Transaction } from '~/types'

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
  const tournaments = ref<Tournament[]>([])

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

    if (portfoliosRequest.data.length === 0) {
      const createPortfolioRequest = await fintasy.createPortfolio({ name: 'Default Portfolio' })
      if (createPortfolioRequest.code !== 200)
        return

      portfolio.value.available = [createPortfolioRequest.data]
    }

    await refreshTransactions()
  }

  async function refreshTransactions() {
    if (portfolio.value.available.length === 0)
      return

    const portfolioUUID = portfolio.value.available[portfolio.value.active].uuid
    const transactionsRequest = await fintasy.getTransactions({ portfolio: portfolioUUID, limit: 999 })
    if (transactionsRequest.code !== 200)
      return

    transactions.value = transactionsRequest.data
      .toSorted((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
  }

  async function refreshTournaments() {
    const tournamentsRequest = await fintasy.getTournaments({ limit: 999 })
    if (tournamentsRequest.code !== 200)
      return

    tournaments.value = tournamentsRequest.data
      .toSorted((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
  }

  async function refreshAll() {
    await refreshUser()
    await refreshPortfolios()
    await refreshTransactions()
    await refreshTournaments()
  }

  watch(() => user.value.uuid, refreshAll)
  watch(() => portfolio.value.active, refreshTransactions)

  return {
    user,
    portfolio,
    transactions,
    tournaments,
    refresh: {
      all: refreshAll,
      user: refreshUser,
      portfolios: refreshPortfolios,
      transactions: refreshTransactions,
      tournaments: refreshTournaments,
    },
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useStateStore as any, import.meta.hot))
