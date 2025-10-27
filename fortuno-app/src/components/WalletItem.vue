<script lang="ts" setup>
import { formatCoinBR } from 'src/boot/format';
import type { IWallet } from 'src/types/IWallet'
import { useRouter } from 'vue-router';

const router = useRouter()

const props = defineProps<{
  wallet: IWallet
  dense?: boolean
}>()

const openDetail = async () => {
  await router.push(`/wallet/${props.wallet.code}`)
}
</script>

<template>
  <div v-if="!dense" class="wallet-item" @click="openDetail">
    <div class="wallet-item-icon-box">
      <q-icon :name="wallet.type == 'credit_card' ? 'wallet' : 'account_balance'" color="white" />
    </div>
    <div style="display: flex; flex-grow: 1; flex-direction: column;">
      <div class="wallet-item-title" style="font-weight: 700;">{{ wallet.name }}</div>
      <div class="wallet-item-title">
        <span v-if="wallet.type === 'credit_card'">Fatura: {{ formatCoinBR((wallet?.balance?.totalDebit ?? 0) * -1)  }}</span>
        <span v-else>Saldo: {{ formatCoinBR(wallet?.balance?.totalCredit ?? 0) }}</span>
      </div>
      <div v-if="wallet.type === 'credit_card'" class="wallet-item-info">
        Vencimento: {{ wallet.creditCardExpirationDay }} / Melhoria dia: {{ wallet.creditCardCloseDay }}
      </div>
    </div>
    <q-icon class="wallet-item-next" name="arrow_forward" size="24px" />
  </div>
  <div v-else class="wallet-item" @click="openDetail">
    <div>
      <div class="wallet-item-title wrap-word" style="font-weight: 700;">{{ wallet.name }}</div>
      <div class="wallet-item-title">
        {{ wallet.type === 'credit_card' ? formatCoinBR((wallet?.balance?.totalDebit ?? 0) * -1) : formatCoinBR(wallet?.balance?.totalCredit ?? 0) }}
      </div>
    </div>
  </div>
</template>

<style lang="sass" scoped>
.wallet-item
  background-color: #EEEEEE
  border-radius: 8px
  padding: 12px
  display: flex
  flex-wrap: nowrap
  font-size: 16px
  align-items: center
  cursor: pointer
  margin-bottom: 16px
  &-next
    transition: left 0.2 ease-in-out
  &-title
    font-size: 14px
    line-height: 16px
    font-family: Inter
  &-info
    font-size: 12px
  &-icon-box
    background-color: #38414F
    padding: 4px
    border-radius: 8px
    margin-right: 8px
    width: 50px
    height: 50px
    display: flex
    justify-content: center
    align-items: center
    .q-icon
      font-size: 32px
  &:hover
    background-color: #d2d1d1

</style>
