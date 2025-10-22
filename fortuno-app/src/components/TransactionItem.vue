<script setup lang="ts">
import { formatCoinBR } from 'src/boot/format';
import type { ITransaction } from 'src/types/ITransacation';

defineProps<{
  transaction: ITransaction
  hideWallet?: boolean
}>()
</script>
<template>
  <div class="transaction-item row align-center" @click="$emit('click')">
    <div class="transaction-item-icon" :style="{ backgroundColor: transaction.category?.color }">
      <q-icon :name="transaction.category?.icon" size="16px" />
    </div>
    <div class="q-pl-sm">
      <div class="text-subtitle2">{{ transaction.name }}
        <span v-if="!hideWallet">({{ transaction.walletAccount?.name  }})</span>
      </div>
      <div class="text-caption">{{transaction.type == 'debit' ? '-' : ''}}{{ formatCoinBR(transaction.value) }}</div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style lang="sass">
.transaction-item
  cursor: pointer
  &-icon
    width: 40px
    height: 40px
    border-radius: 8px
    display: flex
    justify-content: center
    align-items: center
</style>
