<script setup lang="ts">
import { formatCoinBR } from 'src/boot/format';
import { useWalletStore } from 'src/stores/wallet';
import { computed } from 'vue';

const walletStore = useWalletStore()

const walletDetail = computed(() => walletStore.walletDetail)
</script>
<template>
  <div style="color: white;">
    <div class="text-center text-h5 text-weight-bold text-white q-mt-xs q-mb-sm">
      {{ walletDetail.name }}
    </div>
    <div v-if="walletDetail.type == 'credit_card'" class="row text-subtitle1">
      <div class="col-6 text-center q-pr-sm" style="border-right: 1px solid white">
        <div>Fatural atual</div>
        <div>{{ formatCoinBR(walletDetail?.balance?.totalDebit ?? 0) }}</div>
      </div>
      <div class="col-6 text-center q-pl-sm">
        <div>Vencimento: {{ walletDetail?.creditCardExpirationDay }}</div>
        <div>Melhor dia: {{ walletDetail?.creditCardCloseDay }}</div>
      </div>
    </div>
    <div v-else class="row text-subtitle1">
      <div class="col-6 text-green text-center q-pr-sm" style="border-right: 1px solid white">
        <q-icon name="arrow_upward_alt" color="green" class="inline-block" />
        {{ formatCoinBR(walletDetail?.balance?.totalCredit ?? 0)}}
      </div>
      <div class="col-6 text-red text-center q-pl-sm">
        {{ formatCoinBR(walletDetail?.balance?.totalDebit ?? 0)}}
        <q-icon name="arrow_downward_alt" color="red" size="30" class="inline-block" />
      </div>
    </div>
  </div>
</template>