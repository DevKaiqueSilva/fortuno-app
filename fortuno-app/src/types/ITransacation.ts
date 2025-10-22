import type { ICategory } from "./ICategory"
import type { IWallet } from "./IWallet"

export interface ITransaction {
  code: string
  name: string
  value: number
  type: "credit" | "debit"
  status: "pending" | "canceled" | "paid" | "draft"
  originatedAt: string
  description: string
  installmentsEnabled: boolean
  installments: number
  currentInstallment?: number
  walletAccount?: IWallet
  walletAccountCode?: string
  category?: ICategory
  categoryCode?: string
}

export interface ITransactionFilter {
  page:  number,
  pageSize: number
  search: string
  walletCode: string
  month: number
  year: number
}