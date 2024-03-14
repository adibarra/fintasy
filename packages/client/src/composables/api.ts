import type { UseFetchReturn } from '@vueuse/core'

export function useAPI() {
  const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:3332/api/v1'
  const sessionToken = useSessionStorage('session-token', '')

  function checkResponse<T extends keyof API_RESPONSE>(response: UseFetchReturn<API_RESPONSE[T]>): API_RESPONSE[T] {
    if (response.statusCode.value === null)
      return { code: null, message: 'Request Timed Out' }
    if (response.data.value === null)
      return { code: null, message: 'Request Failed' }
    return response.data.value
  }

  return {
    login: async (email: string, password: string): Promise<API_RESPONSE[API_QUERY.POST_SESSION]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.POST_SESSION]>(`${API_BASE}/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })
      const data = checkResponse<API_QUERY.POST_SESSION>(response)
      if (data.code === 200)
        sessionToken.value = data.data?.token ?? ''
      return data
    },
    logout: async (): Promise<API_RESPONSE[API_QUERY.DELETE_SESSION]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.DELETE_SESSION]>(`${API_BASE}/sessions`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      })
      const data = checkResponse<API_QUERY.DELETE_SESSION>(response)
      if (data.code === 200)
        sessionToken.value = ''
      return data
    },
    createUser: async (email: string, username: string, password: string): Promise<API_RESPONSE[API_QUERY.POST_USER]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.POST_USER]>(`${API_BASE}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, username, password }),
      })
      return checkResponse<API_QUERY.POST_USER>(response)
    },
    getUser: async (uuid: string): Promise<API_RESPONSE[API_QUERY.GET_USER]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.GET_USER]>(`${API_BASE}/users/${uuid}`, {
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      })
      return checkResponse<API_QUERY.GET_USER>(response)
    },
    updateUser: async (uuid: string, email?: string, username?: string, password?: string): Promise<API_RESPONSE[API_QUERY.PATCH_USER]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.PATCH_USER]>(`${API_BASE}/users/${uuid}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sessionToken.value}`,
        },
        body: JSON.stringify({ email, username, password }),
      })
      return checkResponse<API_QUERY.PATCH_USER>(response)
    },
    deleteUser: async (uuid: string): Promise<API_RESPONSE[API_QUERY.DELETE_USER]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.DELETE_USER]>(`${API_BASE}/users/${uuid}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      })
      return checkResponse<API_QUERY.DELETE_USER>(response)
    },
    createPortfolio: async (name: string, tournament: string): Promise<API_RESPONSE[API_QUERY.POST_PORTFOLIO]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.POST_PORTFOLIO]>(`${API_BASE}/portfolios`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sessionToken.value}`,
        },
        body: JSON.stringify({ name, tournament }),
      })
      return checkResponse<API_QUERY.POST_PORTFOLIO>(response)
    },
    getPortfolio: async (uuid: string): Promise<API_RESPONSE[API_QUERY.GET_PORTFOLIO]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.GET_PORTFOLIO]>(`${API_BASE}/portfolios/${uuid}`, {
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      })
      return checkResponse<API_QUERY.GET_PORTFOLIO>(response)
    },
    updatePortfolio: async (uuid: string, name?: string): Promise<API_RESPONSE[API_QUERY.PATCH_PORTFOLIO]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.PATCH_PORTFOLIO]>(`${API_BASE}/portfolios/${uuid}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sessionToken.value}`,
        },
        body: JSON.stringify({ name }),
      })
      return checkResponse<API_QUERY.PATCH_PORTFOLIO>(response)
    },
    deletePortfolio: async (uuid: string): Promise<API_RESPONSE[API_QUERY.DELETE_PORTFOLIO]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.DELETE_PORTFOLIO]>(`${API_BASE}/portfolios/${uuid}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      })
      return checkResponse<API_QUERY.DELETE_PORTFOLIO>(response)
    },
    getPortfolios: async (owner: string, offset?: number, limit?: number): Promise<API_RESPONSE[API_QUERY.GET_PORTFOLIOS_USER]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.GET_PORTFOLIOS_USER]>(`${API_BASE}/portfolios/user/${owner}&offset=${offset}&limit=${limit}`, {
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      })
      return checkResponse<API_QUERY.GET_PORTFOLIOS_USER>(response)
    },
    createTransaction: async (portfolio: string, symbol: string, action: string, quantity: number): Promise<API_RESPONSE[API_QUERY.POST_TRANSACTION]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.POST_TRANSACTION]>(`${API_BASE}/transactions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sessionToken.value}`,
        },
        body: JSON.stringify({ portfolio, symbol, action, quantity }),
      })
      return checkResponse<API_QUERY.POST_TRANSACTION>(response)
    },
    getTransaction: async (uuid: string): Promise<API_RESPONSE[API_QUERY.GET_TRANSACTION]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.GET_TRANSACTION]>(`${API_BASE}/transactions/${uuid}`, {
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      })
      return checkResponse<API_QUERY.GET_TRANSACTION>(response)
    },
    getTransactions: async (portfolio: string, offset?: number, limit?: number): Promise<API_RESPONSE[API_QUERY.GET_TRANSACTIONS_PORTFOLIO]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.GET_TRANSACTIONS_PORTFOLIO]>(`${API_BASE}/transactions/portfolio/${portfolio}&offset=${offset}&limit=${limit}`, {
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      })
      return checkResponse<API_QUERY.GET_TRANSACTIONS_PORTFOLIO>(response)
    },
    getQuote: async (symbol: string): Promise<API_RESPONSE[API_QUERY.GET_QUOTE]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.GET_QUOTE]>(`${API_BASE}/quotes/${symbol}`, {
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      })
      return checkResponse<API_QUERY.GET_QUOTE>(response)
    },
  }

  enum API_QUERY {
    POST_SESSION, DELETE_SESSION,
    POST_USER, GET_USER, PATCH_USER, DELETE_USER,
    POST_PORTFOLIO, GET_PORTFOLIO, PATCH_PORTFOLIO, DELETE_PORTFOLIO, GET_PORTFOLIOS_USER,
    POST_TRANSACTION, GET_TRANSACTION, GET_TRANSACTIONS_PORTFOLIO,
    GET_QUOTE,
  }

  interface API_RESPONSE {
    [API_QUERY.POST_SESSION]: {
      code: null | 200 | 400 | 401 | 404 | 500
      message: string
      data?: {
        token: string
      }
    }
    [API_QUERY.DELETE_SESSION]: {
      code: null | 200 | 400 | 401 | 404 | 500
      message: string
    }
    [API_QUERY.POST_USER]: {
      code: null | 200 | 400 | 401 | 404 | 500
      message: string
    }
    [API_QUERY.GET_USER]: {
      code: null | 200 | 400 | 401 | 404 | 500
      message: string
      data?: {
        uuid: string
        email: string
        username: string
        coins: number
        created_at: string
        updated_at: string
      }
    }
    [API_QUERY.PATCH_USER]: {
      code: null | 200 | 400 | 401 | 404 | 500
      message: string
    }
    [API_QUERY.DELETE_USER]: {
      code: null | 200 | 400 | 401 | 404 | 500
      message: string
    }
    [API_QUERY.POST_PORTFOLIO]: {
      code: null | 200 | 400 | 401 | 404 | 500
      message: string
    }
    [API_QUERY.GET_PORTFOLIO]: {
      code: null | 200 | 400 | 401 | 404 | 500
      message: string
      data?: {
        uuid: string
        owner: string
        tournament: string
        name: string
        balance_cents: number
        created_at: string
        updated_at: string
      }
    }
    [API_QUERY.PATCH_PORTFOLIO]: {
      code: null | 200 | 400 | 401 | 404 | 500
      message: string
    }
    [API_QUERY.DELETE_PORTFOLIO]: {
      code: null | 200 | 400 | 401 | 404 | 500
      message: string
    }
    [API_QUERY.GET_PORTFOLIOS_USER]: {
      code: null | 200 | 400 | 401 | 404 | 500
      message: string
      data?: {
        uuid: string
        owner: string
        tournament: string
        name: string
        balance_cents: number
        created_at: string
        updated_at: string
      }[]
    }
    [API_QUERY.POST_TRANSACTION]: {
      code: null | 200 | 400 | 401 | 404 | 500
      message: string
    }
    [API_QUERY.GET_TRANSACTION]: {
      code: null | 200 | 400 | 401 | 404 | 500
      message: string
      data?: {
        uuid: string
        portfolio: string
        symbol: string
        action: string
        quantity: number
        price_cents: number
        created_at: string
      }
    }
    [API_QUERY.GET_TRANSACTIONS_PORTFOLIO]: {
      code: null | 200 | 400 | 401 | 404 | 500
      message: string
      data?: {
        uuid: string
        portfolio: string
        symbol: string
        action: string
        quantity: number
        price_cents: number
        created_at: string
      }[]
    }
    [API_QUERY.GET_QUOTE]: {
      code: null | 200 | 400 | 401 | 404 | 500
      message: string
      data?: {
        symbol: string
        price_cents: number
        timestamp: string
      }
    }
  }
}
