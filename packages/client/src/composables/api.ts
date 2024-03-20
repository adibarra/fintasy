import type { UseFetchReturn } from '@vueuse/core'

/**
 * Composable function to use the Fintasy API
 * @returns an object with functions to interact with the API
 */
export function useAPI() {
  const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:3332/api/v1'
  const sessionToken = useSessionStorage('session-token', '')

  enum API_QUERY {
    POST_SESSION, DELETE_SESSION,
    POST_USER, GET_USER, PATCH_USER, DELETE_USER,
    POST_PORTFOLIO, GET_PORTFOLIOS, GET_PORTFOLIO, PATCH_PORTFOLIO, DELETE_PORTFOLIO,
    POST_TRANSACTION, GET_TRANSACTIONS, GET_TRANSACTION,
    POST_TOURNAMENT, GET_TOURNAMENTS, GET_TOURNAMENT, PATCH_TOURNAMENT, DELETE_TOURNAMENT,
    GET_QUOTE,
  }

  return {
    /**
     * Login to the API and store the session token
     * @param data
     * @param data.email the user's email
     * @param data.password the user's password
     */
    login: async (data: { email: string, password: string }) => {
      const response = await useFetch(`${API_BASE}/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      }, {
        afterFetch: (ctx) => {
          sessionToken.value = ctx.data.data.token
          return ctx
        },
      }).json<API_RESPONSE[API_QUERY.POST_SESSION]>()
      return handleErrors<API_QUERY.POST_SESSION>(response)
    },
    /**
     * Logout of the API and remove the session token
     */
    logout: async (): Promise<API_RESPONSE[API_QUERY.DELETE_SESSION]> => {
      const response = await useFetch(`${API_BASE}/sessions`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      }, {
        afterFetch: (ctx) => {
          sessionToken.value = ''
          return ctx
        },
      }).json<API_RESPONSE[API_QUERY.DELETE_SESSION]>()
      return handleErrors<API_QUERY.DELETE_SESSION>(response)
    },
    /**
     * Create a new user
     * @param data
     * @param data.email The user's email
     * @param data.username The user's username
     * @param data.password The user's password
     */
    createUser: async (data: { email: string, username: string, password: string }): Promise<API_RESPONSE[API_QUERY.POST_USER]> => {
      const response = await useFetch(`${API_BASE}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      }).json<API_RESPONSE[API_QUERY.POST_USER]>()
      return handleErrors<API_QUERY.POST_USER>(response)
    },
    /**
     * Get user information
     * @param data
     * @param data.uuid the user's UUID
     */
    getUser: async (data: { uuid: string }): Promise<API_RESPONSE[API_QUERY.GET_USER]> => {
      const response = await useFetch(`${API_BASE}/users/${data.uuid}`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      }).json<API_RESPONSE[API_QUERY.GET_USER]>()
      return handleErrors<API_QUERY.GET_USER>(response)
    },
    /**
     * Update user information
     * @param data
     * @param data.uuid the user's UUID
     * @param data.email (optional) the user's new email
     * @param data.username (optional) the user's new username
     * @param data.password (optional) the user's new password
     */
    updateUser: async (data: { uuid: string, email?: string, username?: string, password?: string }): Promise<API_RESPONSE[API_QUERY.PATCH_USER]> => {
      const response = await useFetch(`${API_BASE}/users/${data.uuid}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sessionToken.value}`,
        },
        body: JSON.stringify({ email: data.email, username: data.username, password: data.password }),
      }).json<API_RESPONSE[API_QUERY.PATCH_USER]>()
      return handleErrors<API_QUERY.PATCH_USER>(response)
    },
    /**
     * Delete a user
     * @param data
     * @param data.uuid the user's UUID
     */
    deleteUser: async (data: { uuid: string }): Promise<API_RESPONSE[API_QUERY.DELETE_USER]> => {
      const response = await useFetch(`${API_BASE}/users/${data.uuid}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      }).json<API_RESPONSE[API_QUERY.DELETE_USER]>()
      return handleErrors<API_QUERY.DELETE_USER>(response)
    },
    /**
     * Create a new portfolio
     * @param data
     * @param data.name the portfolio name
     * @param data.tournament (optional) the tournament UUID
     */
    createPortfolio: async (data: { name: string, tournament?: string }): Promise<API_RESPONSE[API_QUERY.POST_PORTFOLIO]> => {
      const response = await useFetch(`${API_BASE}/portfolios`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sessionToken.value}`,
        },
        body: JSON.stringify(removeEmpty(data)),
      }).json<API_RESPONSE[API_QUERY.POST_PORTFOLIO]>()
      return handleErrors<API_QUERY.POST_PORTFOLIO>(response)
    },
    /**
     * Get all portfolios which match filers
     * @param data
     * @param data.owner (optional) the user's UUID
     * @param data.tournament (optional) the tournament UUID
     * @param data.name (optional) the portfolio name
     * @param data.offset (optional) the offset to start returning portfolios from
     * @param data.limit (optional) the maximum number of portfolios to return
     */
    getPortfolios: async (data: { owner?: string, tournament?: string, name?: string, offset?: number, limit?: number }): Promise<API_RESPONSE[API_QUERY.GET_PORTFOLIOS]> => {
      const params = new URLSearchParams(removeEmpty(data))
      const response = await useFetch(`${API_BASE}/portfolios?${params}`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      }).json<API_RESPONSE[API_QUERY.GET_PORTFOLIOS]>()
      return handleErrors<API_QUERY.GET_PORTFOLIOS>(response)
    },
    /**
     * Get portfolio information
     * @param data
     * @param data.uuid the portfolio UUID
     */
    getPortfolio: async (data: { uuid: string }): Promise<API_RESPONSE[API_QUERY.GET_PORTFOLIO]> => {
      const response = await useFetch(`${API_BASE}/portfolios/${data.uuid}`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      }).json<API_RESPONSE[API_QUERY.GET_PORTFOLIO]>()
      return handleErrors<API_QUERY.GET_PORTFOLIO>(response)
    },
    /**
     * Update portfolio information
     * @param data
     * @param data.uuid the portfolio UUID
     * @param data.name (optional) the portfolio name
     */
    updatePortfolio: async (data: { uuid: string, name?: string }): Promise<API_RESPONSE[API_QUERY.PATCH_PORTFOLIO]> => {
      const response = await useFetch(`${API_BASE}/portfolios/${data.uuid}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sessionToken.value}`,
        },
        body: JSON.stringify({ name: data.name }),
      }).json<API_RESPONSE[API_QUERY.PATCH_PORTFOLIO]>()
      return handleErrors<API_QUERY.PATCH_PORTFOLIO>(response)
    },
    /**
     * Delete a portfolio
     * @param data
     * @param data.uuid the portfolio UUID
     */
    deletePortfolio: async (data: { uuid: string }): Promise<API_RESPONSE[API_QUERY.DELETE_PORTFOLIO]> => {
      const response = await useFetch(`${API_BASE}/portfolios/${data.uuid}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      }).json<API_RESPONSE[API_QUERY.DELETE_PORTFOLIO]>()
      return handleErrors<API_QUERY.DELETE_PORTFOLIO>(response)
    },
    /**
     * Create a new transaction
     * @param data
     * @param data.portfolio the portfolio UUID
     * @param data.symbol the stock symbol
     * @param data.action the transaction action (BUY or SELL)
     * @param data.quantity the number of shares
     */
    createTransaction: async (data: { portfolio: string, symbol: string, action: ACTION, quantity: number }): Promise<API_RESPONSE[API_QUERY.POST_TRANSACTION]> => {
      const response = await useFetch(`${API_BASE}/transactions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sessionToken.value}`,
        },
        body: JSON.stringify(data),
      }).json<API_RESPONSE[API_QUERY.POST_TRANSACTION]>()
      return handleErrors<API_QUERY.POST_TRANSACTION>(response)
    },
    /**
     * Get all transactions which match filters
     * @param data
     * @param data.portfolio the portfolio UUID
     * @param data.offset (optional) the offset to start returning transactions from
     * @param data.limit (optional) the maximum number of transactions to return
     */
    getTransactions: async (data: { portfolio: string, offset?: number, limit?: number }): Promise<API_RESPONSE[API_QUERY.GET_TRANSACTIONS]> => {
      const params = new URLSearchParams(removeEmpty(data))
      const response = await useFetch(`${API_BASE}/transactions?${params}`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      }).json<API_RESPONSE[API_QUERY.GET_TRANSACTIONS]>()
      return handleErrors<API_QUERY.GET_TRANSACTIONS>(response)
    },
    /**
     * Get transaction information
     * @param data
     * @param data.uuid the transaction UUID
     */
    getTransaction: async (data: { uuid: string }): Promise<API_RESPONSE[API_QUERY.GET_TRANSACTION]> => {
      const response = await useFetch(`${API_BASE}/transactions/${data.uuid}`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      }).json<API_RESPONSE[API_QUERY.GET_TRANSACTION]>()
      return handleErrors<API_QUERY.GET_TRANSACTION>(response)
    },
    /**
     * Create a new tournament
     * @param data
     * @param data.name the tournament name
     * @param data.start_date the tournament start date
     * @param data.end_date the tournament end date
     */
    createTournament: async (data: { name: string, start_date: string, end_date: string }): Promise<API_RESPONSE[API_QUERY.POST_TOURNAMENT]> => {
      const response = await useFetch(`${API_BASE}/tournaments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sessionToken.value}`,
        },
        body: JSON.stringify(data),
      }).json<API_RESPONSE[API_QUERY.POST_TOURNAMENT]>()
      return handleErrors<API_QUERY.POST_TOURNAMENT>(response)
    },
    /**
     * Get all tournaments which match filters
     * @param data
     * @param data.owner (optional) the owner's UUID
     * @param data.name (optional) the tournament name
     * @param data.status (optional) the tournament status
     * @param data.start_date (optional) the start date to filter tournaments from
     * @param data.end_date (optional) the end date to filter tournaments from
     * @param data.offset (optional) the offset to start returning tournaments from
     * @param data.limit (optional) the maximum number of tournaments to return
     */
    getTournaments: async (data: { owner?: string, name?: string, status?: STATUS, start_date?: string, end_date?: string, offset?: number, limit?: number }): Promise<API_RESPONSE[API_QUERY.GET_TOURNAMENTS]> => {
      const params = new URLSearchParams(removeEmpty(data))
      const response = await useFetch(`${API_BASE}/tournaments?${params}`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      }).json<API_RESPONSE[API_QUERY.GET_TOURNAMENTS]>()
      return handleErrors<API_QUERY.GET_TOURNAMENTS>(response)
    },
    /**
     * Get tournament information
     * @param data
     * @param data.uuid the tournament UUID
     */
    getTournament: async (data: { uuid: string }): Promise<API_RESPONSE[API_QUERY.GET_TOURNAMENT]> => {
      const response = await useFetch(`${API_BASE}/tournaments/${data.uuid}`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      }).json<API_RESPONSE[API_QUERY.GET_TOURNAMENT]>()
      return handleErrors<API_QUERY.GET_TOURNAMENT>(response)
    },
    /**
     * Update tournament information
     * @param data
     * @param data.uuid the tournament UUID
     * @param data.name the tournament name
     * @param data.start_date the tournament start date
     * @param data.end_date the tournament end date
     */
    updateTournament: async (data: { uuid: string, name?: string, start_date?: string, end_date?: string }): Promise<API_RESPONSE[API_QUERY.PATCH_TOURNAMENT]> => {
      const response = await useFetch(`${API_BASE}/tournaments/${data.uuid}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sessionToken.value}`,
        },
        body: JSON.stringify({ name: data.name, start_date: data.start_date, end_date: data.end_date }),
      }).json<API_RESPONSE[API_QUERY.PATCH_TOURNAMENT]>()
      return handleErrors<API_QUERY.PATCH_TOURNAMENT>(response)
    },
    /**
     * Delete a tournament
     * @param data
     * @param data.uuid the tournament UUID
     */
    deleteTournament: async (data: { uuid: string }): Promise<API_RESPONSE[API_QUERY.DELETE_TOURNAMENT]> => {
      const response = await useFetch(`${API_BASE}/tournaments/${data.uuid}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      }).json<API_RESPONSE[API_QUERY.DELETE_TOURNAMENT]>()
      return handleErrors<API_QUERY.DELETE_TOURNAMENT>(response)
    },
    /**
     * Get the latest quote for a symbol
     * @param data
     * @param data.symbol the stock symbol
     */
    getQuote: async (data: { symbol: string }): Promise<API_RESPONSE[API_QUERY.GET_QUOTE]> => {
      const response = await useFetch(`${API_BASE}/quotes/${data.symbol}`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${sessionToken.value}` },
      }).json<API_RESPONSE[API_QUERY.GET_QUOTE]>()
      return handleErrors<API_QUERY.GET_QUOTE>(response)
    },
  }

  function handleErrors<T extends keyof API_RESPONSE>(response: UseFetchReturn<API_RESPONSE[T]>): API_RESPONSE[T] {
    if (response.statusCode.value === null)
      return { code: null, message: 'Request Timed Out' }
    if (response.data.value === null)
      return { code: null, message: 'Request Failed' }
    return response.data.value
  }

  function removeEmpty(obj: Record<string, any>): Record<string, any> {
    return Object.fromEntries(Object.entries(obj).filter(([_, v]) => v != null))
  }

  type ACTION = 'BUY' | 'SELL'
  type STATUS = 'SCHEDULED' | 'ONGOING' | 'FINISHED'

  interface User {
    uuid: string
    email: string
    username: string
    coins: number
    created_at: string
    updated_at: string
  }

  interface Portfolio {
    uuid: string
    owner: string
    tournament: string
    name: string
    balance_cents: number
    created_at: string
    updated_at: string
  }

  interface Transaction {
    uuid: string
    portfolio: string
    symbol: string
    action: ACTION
    quantity: number
    price_cents: number
    created_at: string
  }

  interface Tournament {
    uuid: string
    owner: string
    name: string
    status: STATUS
    start_date: string
    end_date: string
    created_at: string
    updated_at: string
  }

  interface Quote {
    symbol: string
    price_cents: number
    timestamp: string
  }

  interface Session {
    token: string
    uuid: string
  }

  interface BaseResponse {
    code: 500 | 409 | 404 | 403 | 401 | 400 | 200 | null
    message: string
  }

  interface UnsuccessfulResponse {
    code: 500 | 409 | 404 | 403 | 401 | 400 | null
    message: string
  }

  interface SuccessfulResponse<T> {
    code: 200
    message: string
    data: T
  }

  // https://stackoverflow.com/a/69288824
  // recursively expands the types of objects to see shape instead of type names
  type ExpandRecursively<T> = T extends (...args: infer A) => infer R
    ? (...args: ExpandRecursively<A>) => ExpandRecursively<R>
    : T extends object
      ? T extends infer O
        ? { [K in keyof O]: ExpandRecursively<O[K]> }
        : never
      : T

  interface API_RESPONSE {
    [API_QUERY.POST_SESSION]: ExpandRecursively<SuccessfulResponse<Session> | UnsuccessfulResponse>
    [API_QUERY.DELETE_SESSION]: ExpandRecursively<BaseResponse>
    [API_QUERY.POST_USER]: ExpandRecursively<SuccessfulResponse<User> | UnsuccessfulResponse>
    [API_QUERY.GET_USER]: ExpandRecursively<SuccessfulResponse<User> | UnsuccessfulResponse>
    [API_QUERY.PATCH_USER]: ExpandRecursively<BaseResponse>
    [API_QUERY.DELETE_USER]: ExpandRecursively<BaseResponse>
    [API_QUERY.POST_PORTFOLIO]: ExpandRecursively<SuccessfulResponse<Portfolio> | UnsuccessfulResponse>
    [API_QUERY.GET_PORTFOLIO]: ExpandRecursively<SuccessfulResponse<Portfolio> | UnsuccessfulResponse>
    [API_QUERY.GET_PORTFOLIOS]: ExpandRecursively<SuccessfulResponse<Portfolio[]> | UnsuccessfulResponse>
    [API_QUERY.PATCH_PORTFOLIO]: ExpandRecursively<BaseResponse>
    [API_QUERY.DELETE_PORTFOLIO]: ExpandRecursively<BaseResponse>
    [API_QUERY.POST_TRANSACTION]: ExpandRecursively<SuccessfulResponse<Transaction> | UnsuccessfulResponse>
    [API_QUERY.GET_TRANSACTION]: ExpandRecursively<SuccessfulResponse<Transaction> | UnsuccessfulResponse>
    [API_QUERY.GET_TRANSACTIONS]: ExpandRecursively<SuccessfulResponse<Transaction[]> | UnsuccessfulResponse>
    [API_QUERY.POST_TOURNAMENT]: ExpandRecursively<SuccessfulResponse<Tournament> | UnsuccessfulResponse>
    [API_QUERY.GET_TOURNAMENTS]: ExpandRecursively<SuccessfulResponse<Tournament[]> | UnsuccessfulResponse>
    [API_QUERY.GET_TOURNAMENT]: ExpandRecursively<SuccessfulResponse<Tournament> | UnsuccessfulResponse>
    [API_QUERY.PATCH_TOURNAMENT]: ExpandRecursively<BaseResponse>
    [API_QUERY.DELETE_TOURNAMENT]: ExpandRecursively<BaseResponse>
    [API_QUERY.GET_QUOTE]: ExpandRecursively<SuccessfulResponse<Quote> | UnsuccessfulResponse>
  }
}
