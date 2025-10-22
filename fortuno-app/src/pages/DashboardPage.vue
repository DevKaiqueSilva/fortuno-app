<script setup lang="ts">
import ModalWallet from 'src/components/modal/ModalWallet.vue'
import WalletItem from 'src/components/WalletItem.vue'
import TransactionList from 'src/components/TransactionList.vue'
import ChartCategoryBalance from 'src/components/chart/ChartCategoryBalance.vue'
import { onMounted, ref } from 'vue'
import { useWalletStore } from 'src/stores/wallet'
import { useRouter } from 'vue-router'

const walletStore = useWalletStore()
const router = useRouter()

const showWalletModal = ref(false)

onMounted(async () => {
  await walletStore.fetchWallets()
})
</script>

<template>
  <q-page class="dashboard-page items-center justify-evenly text-dark fit">
    <div class="q-mb-md">
      <div class="text-subtitle1 text-weight-bold">Contas</div>
      <div v-if="walletStore.getWallets.length > 0" class="row">
        <div 
          v-for="(wallet, i) in walletStore.getWallets"
          :key="`wallet-${i}`"
          class="col-4 q q-pa-xs"
        >
          <wallet-item :wallet="wallet" dense key=""/>
        </div>
      </div>
      <q-btn
        v-else
        color="primary"
        label="Nova conta"
        class="fit q-mt-sm"
        text-color="dark"
        @click="showWalletModal = true"
      />
      <ModalWallet v-model="showWalletModal" />
    </div>
    <chart-category-balance class="q-mb-md" />
    <div>
      <div class="text-subtitle1 text-weight-bold q-mb-xs">Últimas transações</div>
      <transaction-list custom-change-page @change-page="router.push('/transactions')" />
    </div>
  </q-page>
</template>

<style lang="sass">
.dashboard
  &-account
    background: #9EA4AE !important
    border-radius: 8px
    padding: 8px
    box-shadow: none
</style>
