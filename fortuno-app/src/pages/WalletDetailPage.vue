<script setup lang="ts">
import FilterMonth from 'src/components/filter/FilterMonth.vue'
import { useTransactionStore } from 'src/stores/transaction'
import TransactionList from 'src/components/TransactionList.vue'
import { useRoute } from 'vue-router'
import { useWalletStore } from 'src/stores/wallet'
import { onMounted } from 'vue'

const transactionStore = useTransactionStore()
const walletStore = useWalletStore()
const route = useRoute()

const changeMonth = async (month: number, year: number) => {
  transactionStore.setFilter({
    ...transactionStore.filter,
    page: 1,
    month,
    year
  })
  transactionStore.resetTransactions()
  await transactionStore.fetchTransactions()
}

onMounted(async () => {
  await walletStore.fetchWalletDetail(route.params.code as string)
})
</script>

<template>
  <div class="text-dark">
    <filter-month @change="changeMonth" />
    <q-separator class="q-my-md" />
    <div class="row q-col-gutter-md">
      <div class="col-12">
        <transaction-list :wallet-code="String(route.params.code)" />
      </div>
    </div>
  </div>
</template>
