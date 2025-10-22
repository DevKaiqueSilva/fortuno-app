import { defineStore } from 'pinia'
import { api } from 'boot/axios'
import type { IWallet } from 'src/types/IWallet'

export const useWalletStore = defineStore('wallet', {
  state: () => ({
    wallets: [] as Array<IWallet>,
    walletDetail: {} as IWallet 
  }),
  getters: {
    getWallets(state) {
      return state.wallets
    }
  },
  actions: {
    async fetchWallets(save: boolean = true) {
      let wallets = [] as Array<IWallet>
      const { data, status } = await api.get('/api/wallet/?page_size=30')
      if (status === 200) {
        wallets = data.results
        if (save) {
          this.wallets = wallets
        } 
      }
      return wallets
    },
    async fetchWalletDetail(walletCode: string) {
      const { data, status } = await api.get(`/api/wallet/${walletCode}/`)
      if (status === 200) {
        this.walletDetail = data
      }
    },
    async saveWallet(wallet: IWallet) {
      let saved = false
      const url = `/api/wallet/${wallet.code ? `${wallet.code}/` : ''}`
      const isCreditCard = wallet.type === 'credit_card'
      const payload = isCreditCard ? {
        ...wallet,
        creditCardLimit: wallet.creditCardLimit
          ? parseFloat(wallet.creditCardLimit.toString().replace('.', '').replace(',', '.'))
          : 0
      } : {
        name: wallet.name,
        type: wallet.type,
      }
      const { status } = await (wallet.code ? api.put(url, payload) : api.post(url, payload))
      if ([200, 201].includes(status)) {
        saved = true
        await this.fetchWallets()
      }
      return saved
    }
  }
})
