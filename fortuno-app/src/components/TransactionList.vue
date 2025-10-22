<script setup lang="ts">
import TransactionItem from 'src/components/TransactionItem.vue'
import { useTransactionStore } from 'src/stores/transaction'
import { computed, onMounted, ref } from 'vue'
import moment from 'moment'
import 'moment/locale/pt-br'
import type { ITransaction } from 'src/types/ITransacation'
import ModalTransaction from './modal/ModalTransaction.vue'

moment.locale('pt-br')

const transactionStore = useTransactionStore()
const emit = defineEmits(['changePage'])

const props = defineProps<{
  walletCode?: string
  pageSize?: number
  customChangePage?: boolean
}>()

const showTransactionModal = ref(false)
const transactionEdit = ref<ITransaction>()

const groupedTransactions = computed(() => {
  const groups: Record<string, Array<ITransaction>> = {}

  transactionStore.transactions.forEach((transaction) => {
    const date = moment(transaction.originatedAt)
    const key = date.format('DD MMM/YY')

    if (!groups[key]) {
      groups[key] = []
    }
    groups[key].push(transaction)
  })

  return Object.entries(groups)
    .sort(([a], [b]) => moment(b, 'DD MMM/YY').valueOf() - moment(a, 'DD MMM/YY').valueOf())
    .map(([date, transactions]) => ({ date, transactions }))
})

const changePage = async () => {
  if (props.customChangePage) {
    emit('changePage')
    return
  }
  transactionStore.setFilter({
    ...transactionStore.filter,
    page: transactionStore.filter.page + 1
  })
  await transactionStore.fetchTransactions()
} 

const onEditTransaction = (transaction: ITransaction) => {
  transactionEdit.value = transaction
  showTransactionModal.value = true
}

onMounted(async () => {
  transactionStore.resetTransactions()
  transactionStore.setFilter({
    ...transactionStore.filter,
    page: 1,
    walletCode: props.walletCode ?? '',
    pageSize: props.pageSize ?? 25
  })
  await transactionStore.fetchTransactions()
})
</script>

<template>
  <div>
    <div v-for="group in groupedTransactions" :key="group.date" class="q-mb-md">
      <div class="text-weight-bold q-mb-sm text-center" style="opacity: 0.7">
        {{ group.date }}
      </div>
      <transaction-item
        v-for="transaction in group.transactions"
        :key="transaction.code"
        :transaction="transaction"
        :hide-wallet="!!walletCode"
        class="q-mb-md"
        @click="onEditTransaction(transaction)"
      />
    </div>
    <modal-transaction v-model:visible="showTransactionModal" :transactionEdit="transactionEdit" />
    <div class="row justify-center">
      <q-btn v-if="transactionStore.hasNextPage" unelevated flat @click="changePage">
        <q-icon name="expand_more" />
      </q-btn>
    </div>
  </div>
</template>