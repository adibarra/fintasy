/**
 * @author: adibarra (Alec Ibarra)
 * @description: Typescript types definitions
 */

import type { ViteSSGContext } from 'vite-ssg'

export type UserModule = (ctx: ViteSSGContext) => void

export enum ACTION { BUY, SELL }
export enum STATUS { SCHEDULED, ONGOING, FINISHED }

export interface User {
  uuid: string
  email: string
  username: string
  coins: number
  created_at: string
  updated_at: string
}

export interface Portfolio {
  uuid: string
  owner: string
  tournament: string
  name: string
  balance_cents: number
  created_at: string
  updated_at: string
}

export interface Transaction {
  uuid: string
  portfolio: string
  symbol: string
  action: ACTION
  quantity: number
  price_cents: number
  created_at: string
}

export interface Tournament {
  uuid: string
  owner: string
  name: string
  status: STATUS
  start_date: string
  end_date: string
  created_at: string
  updated_at: string
}

export interface Quote {
  symbol: string
  price_cents: number
  timestamp: string
}

export interface Session {
  token: string
  uuid: string
}
