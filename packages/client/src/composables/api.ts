import type { UseFetchReturn } from '@vueuse/core'

export function useAPI() {
  const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:3332/api/v1'
  const sessionToken = useSessionStorage('session-token', '')

  enum API_QUERY {
    POST_SESSION, DELETE_SESSION,
    POST_USER, GET_USER, PATCH_USER, DELETE_USER,
    POST_PORTFOLIO, GET_PORTFOLIO, PATCH_PORTFOLIO, DELETE_PORTFOLIO, GET_PORTFOLIOS_USER,
    POST_TRANSACTION, GET_TRANSACTION, GET_TRANSACTIONS_PORTFOLIO,
    GET_QUOTE,
  }

  enum ACTION {
    BUY = 'BUY',
    SELL = 'SELL',
  }

  return {
    /**
     * Login to the API and store the session token
     * @param email the user's email
     * @param password the user's password
     */
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
    /**
     * Logout of the API and remove the session token
     */
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
    /**
     * Create a new user
     * @param email the user's email
     * @param username the user's username
     * @param password the user's password
     */
    createUser: async (email: string, username: string, password: string): Promise<API_RESPONSE[API_QUERY.POST_USER]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.POST_USER]>(`${API_BASE}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, username, password }),
      })
      return checkResponse<API_QUERY.POST_USER>(response)
    },
    /**
     * Get user information
     * @param uuid the user's UUID
     */
    getUser: async (uuid: string): Promise<API_RESPONSE[API_QUERY.GET_USER]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.GET_USER]>(`${API_BASE}/users/${uuid}`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      })
      return checkResponse<API_QUERY.GET_USER>(response)
    },
    /**
     * Update user information
     * @param uuid the user's UUID
     * @param email the user's email
     * @param username the user's username
     * @param password the user's password
     */
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
    /**
     * Delete a user
     * @param uuid the user's UUID
     */
    deleteUser: async (uuid: string): Promise<API_RESPONSE[API_QUERY.DELETE_USER]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.DELETE_USER]>(`${API_BASE}/users/${uuid}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      })
      return checkResponse<API_QUERY.DELETE_USER>(response)
    },
    /**
     * Create a new portfolio
     * @param name the portfolio name
     * @param tournament the tournament UUID (optional)
     */
    createPortfolio: async (name: string, tournament?: string): Promise<API_RESPONSE[API_QUERY.POST_PORTFOLIO]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.POST_PORTFOLIO]>(`${API_BASE}/portfolios`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sessionToken.value}`,
        },
        body: JSON.stringify(tournament ? { name, tournament } : { name }),
      })
      return checkResponse<API_QUERY.POST_PORTFOLIO>(response)
    },
    /**
     * Get portfolio information
     * @param uuid the portfolio UUID
     */
    getPortfolio: async (uuid: string): Promise<API_RESPONSE[API_QUERY.GET_PORTFOLIO]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.GET_PORTFOLIO]>(`${API_BASE}/portfolios/${uuid}`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      })
      return checkResponse<API_QUERY.GET_PORTFOLIO>(response)
    },
    /**
     * Update portfolio information
     * @param uuid the portfolio UUID
     * @param name the portfolio name
     */
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
    /**
     * Delete a portfolio
     * @param uuid the portfolio UUID
     */
    deletePortfolio: async (uuid: string): Promise<API_RESPONSE[API_QUERY.DELETE_PORTFOLIO]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.DELETE_PORTFOLIO]>(`${API_BASE}/portfolios/${uuid}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      })
      return checkResponse<API_QUERY.DELETE_PORTFOLIO>(response)
    },
    /**
     * Get all portfolios owned by a user
     * @param owner the user's UUID
     * @param offset the offset to start returning portfolios from
     * @param limit the maximum number of portfolios to return
     */
    getPortfolios: async (owner: string, offset?: number, limit?: number): Promise<API_RESPONSE[API_QUERY.GET_PORTFOLIOS_USER]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.GET_PORTFOLIOS_USER]>(`${API_BASE}/portfolios/user/${owner}&offset=${offset}&limit=${limit}`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      })
      return checkResponse<API_QUERY.GET_PORTFOLIOS_USER>(response)
    },
    /**
     * Create a new transaction
     * @param portfolio the portfolio UUID
     * @param symbol the stock symbol
     * @param action the transaction action (BUY or SELL)
     * @param quantity the number of shares
     */
    createTransaction: async (portfolio: string, symbol: string, action: ACTION, quantity: number): Promise<API_RESPONSE[API_QUERY.POST_TRANSACTION]> => {
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
    /**
     * Get transaction information
     * @param uuid the transaction UUID
     */
    getTransaction: async (uuid: string): Promise<API_RESPONSE[API_QUERY.GET_TRANSACTION]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.GET_TRANSACTION]>(`${API_BASE}/transactions/${uuid}`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      })
      return checkResponse<API_QUERY.GET_TRANSACTION>(response)
    },
    /**
     * Get all transactions for a portfolio
     * @param portfolio the portfolio UUID
     * @param offset the offset to start returning transactions from
     * @param limit the maximum number of transactions to return
     */
    getTransactions: async (portfolio: string, offset?: number, limit?: number): Promise<API_RESPONSE[API_QUERY.GET_TRANSACTIONS_PORTFOLIO]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.GET_TRANSACTIONS_PORTFOLIO]>(`${API_BASE}/transactions/portfolio/${portfolio}&offset=${offset}&limit=${limit}`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      })
      return checkResponse<API_QUERY.GET_TRANSACTIONS_PORTFOLIO>(response)
    },
    /**
     * Get the latest quote for a symbol
     * @param symbol the stock symbol
     */
    getQuote: async (symbol: string): Promise<API_RESPONSE[API_QUERY.GET_QUOTE]> => {
      const response = await useFetch<API_RESPONSE[API_QUERY.GET_QUOTE]>(`${API_BASE}/quotes/${symbol}`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      })
      return checkResponse<API_QUERY.GET_QUOTE>(response)
    },
  }

  function checkResponse<T extends keyof API_RESPONSE>(response: UseFetchReturn<API_RESPONSE[T]>): API_RESPONSE[T] {
    if (response.statusCode.value === null)
      return { code: null, message: 'Request Timed Out' }
    if (response.data.value === null)
      return { code: null, message: 'Request Failed' }
    return response.data.value
  }

  interface API_RESPONSE {
    [API_QUERY.POST_SESSION]: {
      code: null | 200 | 400 | 401 | 403 | 404 | 409 | 500
      message: string
      data?: {
        token: string
      }
    }
    [API_QUERY.DELETE_SESSION]: {
      code: null | 200 | 400 | 401 | 403 | 404 | 409 | 500
      message: string
    }
    [API_QUERY.POST_USER]: {
      code: null | 200 | 400 | 401 | 403 | 404 | 409 | 500
      message: string
    }
    [API_QUERY.GET_USER]: {
      code: null | 200 | 400 | 401 | 403 | 404 | 409 | 500
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
      code: null | 200 | 400 | 401 | 403 | 404 | 409 | 500
      message: string
    }
    [API_QUERY.DELETE_USER]: {
      code: null | 200 | 400 | 401 | 403 | 404 | 409 | 500
      message: string
    }
    [API_QUERY.POST_PORTFOLIO]: {
      code: null | 200 | 400 | 401 | 403 | 404 | 409 | 500
      message: string
    }
    [API_QUERY.GET_PORTFOLIO]: {
      code: null | 200 | 400 | 401 | 403 | 404 | 409 | 500
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
      code: null | 200 | 400 | 401 | 403 | 404 | 409 | 500
      message: string
    }
    [API_QUERY.DELETE_PORTFOLIO]: {
      code: null | 200 | 400 | 401 | 403 | 404 | 409 | 500
      message: string
    }
    [API_QUERY.GET_PORTFOLIOS_USER]: {
      code: null | 200 | 400 | 401 | 403 | 404 | 409 | 500
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
      code: null | 200 | 400 | 401 | 403 | 404 | 409 | 500
      message: string
    }
    [API_QUERY.GET_TRANSACTION]: {
      code: null | 200 | 400 | 401 | 403 | 404 | 409 | 500
      message: string
      data?: {
        uuid: string
        portfolio: string
        symbol: string
        action: ACTION
        quantity: number
        price_cents: number
        created_at: string
      }
    }
    [API_QUERY.GET_TRANSACTIONS_PORTFOLIO]: {
      code: null | 200 | 400 | 401 | 403 | 404 | 409 | 500
      message: string
      data?: {
        uuid: string
        portfolio: string
        symbol: string
        action: ACTION
        quantity: number
        price_cents: number
        created_at: string
      }[]
    }
    [API_QUERY.GET_QUOTE]: {
      code: null | 200 | 400 | 401 | 403 | 404 | 409 | 500
      message: string
      data?: {
        symbol: string
        price_cents: number
        timestamp: string
      }
    }
  }
}
