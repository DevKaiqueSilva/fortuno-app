<script lang="ts" setup>
import { useWalletStore } from 'src/stores/wallet'
import { onMounted, ref } from 'vue'
import WalletItem from 'src/components/WalletItem.vue'
import ModalWallet from 'src/components/modal/ModalWallet.vue'

const walletStore = useWalletStore()
const showWalletModal = ref(false)

onMounted(async () => {
  await walletStore.fetchWallets()
})
</script>
<template>
  <q-page class="wallet-page items-center justify-evenly text-dark fit">
    <div class="text-subtitle1 text-weight-bold">Contas</div>
    <wallet-item v-for="(wallet, i) in walletStore.wallets" :key="`wallet-${i}`" :wallet="wallet" />
    <q-btn
      color="primary"
      label="Nova conta"
      class="fit q-mt-sm"
      text-color="dark"
      @click="showWalletModal = true"
    />
    <ModalWallet v-model:visible="showWalletModal" />
  </q-page>
</template>
