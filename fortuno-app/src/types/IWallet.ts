export interface IWallet {
  code: string
  name: string
  type: 'credit_card' | 'bank'
  creditCardLimit: number
  creditCardExpirationDay: number
  creditCardCloseDay: number
  balance?: {
    totalCredit: number
    totalDebit: number
  }
}