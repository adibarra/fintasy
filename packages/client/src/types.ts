/**
 * @author: adibarra (Alec Ibarra)
 * @description: Typescript types definitions
 */

import type { App } from 'vue'
import type { Router } from 'vue-router'

export type UserModule = (ctx: { app: App, router: Router }) => void

export enum ACTION {
  BUY = 'BUY',
  SELL = 'SELL',
}
export enum STATUS {
  SCHEDULED = 'SCHEDULED',
  ONGOING = 'ONGOING',
  FINISHED = 'FINISHED',
}
export enum INTERVAL {
  FIVE_MIN = '5m',
  FIFTEEN_MIN = '15m',
  THIRTY_MIN = '30m',
  ONE_HOUR = '1h',
  ONE_DAY = '1d',
}

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
  owner: string
}
