import { defineStore } from 'pinia'
import { api } from 'boot/axios'
import type { ITransaction, ITransactionFilter } from 'src/types/ITransacation'

export const useTransactionStore = defineStore('transaction', {
  state: () => ({
    filter: {
      page: 1,
      pageSize: 25,
      search: '',
      walletCode: '',
      month: new Date().getMonth() + 1,
      year: new Date().getFullYear(),
      hasNextPage: false
    } as ITransactionFilter,
    transactions: [] as Array<ITransaction>,
    hasNextPage: true,
  }),
  getters: {
    getWallets(state) {
      return state.transactions
    }
  },
  actions: {
    resetTransactions() {
      this.transactions = []
      this.filter.page = 1
      this.hasNextPage = true
    },
    setFilter(filter: ITransactionFilter) {
      this.filter = { ...this.filter, ...filter }
    },
    async fetchTransactions() {
      const query = `page=${this.filter.page}&page_size=${this.filter.pageSize}&wallet_account_code=${this.filter.walletCode}&month=${this.filter.month}&year=${this.filter.year}`
      const { data, status } = await api.get(`/api/transactions/?${query}`)
      if (status === 200) {
        const newTransactions = data.results.filter((newTx: ITransaction) => 
          !this.transactions.some((existingTx: ITransaction) => existingTx.code === newTx.code)
        )
        this.transactions = this.transactions.concat(newTransactions)
        if (this.transactions.length >= data.count) {
          this.hasNextPage = false
        }
      }
    },
    async saveTransaction(transaction: ITransaction) {
      let saved = false
      const url = `/api/transactions/${transaction.code ? `${transaction.code}/` : ''}`
      const payload = {
        name: transaction.name,
        value: transaction.value * 100,
        type: transaction.type,
        status: transaction.status,
        originatedAt: transaction.originatedAt,
        description: "",
        installmentsEnabled: transaction.installmentsEnabled,
        installments: transaction.installments,
        currentInstallment: transaction.currentInstallment ?? 1,
        categoryCode: transaction.categoryCode,
        walletAccountCode: transaction.walletAccountCode,
      }
      const { status } = await (transaction.code ? api.put(url, payload) : api.post(url, payload))
      if ([200, 201].includes(status)) {
        saved = true
        this.resetTransactions()
        await this.fetchTransactions()
      }
      return saved
    },
    async deleteTransaction(transactionCode: string) {
      let deleted = false
      const url = `/api/transactions/${transactionCode}/`
      const { status } = await api.delete(url)
      if (status === 204) {
        deleted = true
        this.resetTransactions()
        await this.fetchTransactions()
      }
      return deleted
    },
  }
})
