<script setup lang="ts">
import { Notify } from 'quasar'
import { useWalletStore } from 'src/stores/wallet'
import type { ITransaction } from 'src/types/ITransacation'
import { rules } from 'src/utils/rules'
import { computed, ref, watch } from 'vue'
import moment from 'moment'
import type { IWallet } from 'src/types/IWallet'
import type { ICategory } from 'src/types/ICategory'
import { useCategoryStore } from 'src/stores/category'
import { useRoute } from 'vue-router'
import { useTransactionStore } from 'src/stores/transaction'

const walletStore = useWalletStore()
const categoryStore = useCategoryStore()
const transactionStore = useTransactionStore()
const route = useRoute()

const visible = defineModel<boolean>('visible', { default: false })

const props = defineProps<{
  transactionEdit?: ITransaction | undefined
}>()

const refTransactionForm = ref()
const transaction = ref<ITransaction>({
  code: '',
  name: '',
  value: 0,
  type: 'credit',
  status: 'pending',
  originatedAt: moment().format('YYYY-MM-DD'),
  description: '',
  installmentsEnabled: false,
  installments: 1,
  walletAccountCode: '',
  categoryCode: '',
})
const loading = ref(false)
const wallets = ref<Array<IWallet>>([])
const categories = ref<Array<ICategory>>([])

watch(transaction,  () => {
  const categoryCode: unknown = transaction.value.categoryCode
  if(categoryCode instanceof Object) {
    transaction.value.categoryCode = (categoryCode as { code: string }).code
  }
  const walletAccountCode: unknown = transaction.value.walletAccountCode
  if(walletAccountCode instanceof Object) {
    transaction.value.walletAccountCode = (walletAccountCode as { code: string }).code
  }
}, {
  deep: true
})

const isBankAccountWallet = computed(() => {
  const wallet = wallets.value.find(w => w.code == transaction.value.walletAccountCode)
  return wallet?.type === 'bank'
})

const onShow = async () => {
  if (visible.value) {
    const transactionEdit = props.transactionEdit
    transaction.value = {
      code: transactionEdit?.code ?? '',
      name: transactionEdit?.name ?? '',
      value: transactionEdit?.value ?? 0,
      type: transactionEdit?.type ?? 'credit',
      status: transactionEdit?.status ?? 'pending',
      originatedAt: moment(transactionEdit?.originatedAt ?? '').format('DD/MM/YYYY'),
      description: transactionEdit?.description ?? '',
      installmentsEnabled: transactionEdit?.installmentsEnabled ?? false,
      installments: transactionEdit?.installments ?? 1,
      walletAccountCode: transactionEdit?.walletAccount?.code ?? (route.name == 'wallet-detail' ? String(route.params.code) : ''),
      categoryCode: transactionEdit?.category?.code ?? '',
    }
    wallets.value = await walletStore.fetchWallets(false)
    categories.value = await categoryStore.fetchCategories(false)
  }
}

const save = async () => {
  const isValid = await refTransactionForm.value.validate()
  if (isValid) {
    let value = transaction.value.value
    if (value) {
      value = parseFloat(value.toString().replace(",", "."))
    }
    loading.value = true
    const result = await transactionStore.saveTransaction({
      ...transaction.value,
      value: value,
      originatedAt: `${transaction.value.originatedAt.split("/").reverse().join("-")}T03:00:00.000Z`,
      type: isBankAccountWallet.value ? transaction.value.type : 'debit'
    })
    if (result) {
      Notify.create({
        type: 'positive',
        message: 'Transação salva com sucesso'
      })
      visible.value = false
    }
    loading.value = false
  } else {
    Notify.create({
      type: 'negative',
      message: 'Verifique os campos obrigatórios'
    })
  }
}

const onDelete = async () => {
  if (!props.transactionEdit) return
  const deleted = await transactionStore.deleteTransaction(props.transactionEdit?.code)
  if (deleted) {
    Notify.create({
      type: 'positive',
      message: 'Transação excluída com sucesso'
    })
    visible.value = false
  } 
}
</script>

<template>
  <q-dialog v-model="visible" @show="onShow">
    <q-card style="width: 450px">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">Nova transação</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>
      <q-card-section>
        <q-form ref="refTransactionForm" @submit="save">
          <q-select 
            v-model="transaction.walletAccountCode"
            filled
            label="Conta"
            class="q-mb-md"
            :rules="[rules.required]"
            lazy-rules
            option-label="name"
            option-value="code"
            map-options
            emit-value
            :options="wallets"
          />
          <q-input
            v-model="transaction.name"
            filled
            label="Nome"
            class="q-mb-md"
            :rules="[rules.required]"
            lazy-rules
            placeholder="Digite um nome para a transação"
          />
          <div v-if="isBankAccountWallet" class="row q-mb-lg">
            <div class="col-6 q-pr-sm">
              <div
                class="transaction-type"
                :class="{ 'transaction-type-active': transaction.type === 'credit' }"
                @click="transaction.type = 'credit'"
              >
                <q-icon name="arrow_upward" />
                Entrada
              </div>
            </div>
            <div class="col-6 q-pl-sm">
              <div
                class="transaction-type"
                :class="{ 'transaction-type-active': transaction.type === 'debit' }"
                @click="transaction.type = 'debit'"
              >
                Saída
                <q-icon name="arrow_downward" />
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-6 q-pr-sm">
              <q-input filled v-model="transaction.originatedAt" mask="##/##/####" :rules="[rules.date]">
                <template v-slot:append>
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                      <q-date v-model="transaction.originatedAt" mask="DD/MM/YYYY">
                        <div class="row items-center justify-end">
                          <q-btn v-close-popup label="Fechar" color="primary" flat />
                        </div>
                      </q-date>
                    </q-popup-proxy>
                  </q-icon>
                </template>
              </q-input>
            </div>
            <div class="col-6 q-pl-sm">
              <q-input
                v-model="transaction.value"
                filled
                label="Valor (R$)"
                mask="#,##"
                fill-mask="0"
                :rules="[rules.required]"
                lazy-rules
                class="q-mb-md"
                reverse-fill-mask
              />
            </div>
          </div>
          <q-select 
            v-model="transaction.categoryCode"
            filled
            label="Categoria"
            :rules="[rules.required]"
            lazy-rules
            option-label="name"
            option-value="code"
            map-options
            :options="categories"
          />
          <q-input
            v-model="transaction.description"
            filled
            label="Observação"
            class="q-my-md"
            placeholder="Tem alguma observação?"
            type="textarea"
          />
          <div v-if="!isBankAccountWallet">
            <q-checkbox 
              v-model="transaction.installmentsEnabled"
              name="installments"
              label="Parcelado"
              class="q-mb-md" 
            />
            <q-input
              v-if="transaction.installmentsEnabled"
              v-model="transaction.installments"
              filled
              label="Parcelas"
              class="q-mb-md"
              :rules="[rules.required]"
              lazy-rules
              type="number"
            />
          </div>
        </q-form>
        <q-btn
          color="primary"
          :label="transactionEdit?.code ? 'Salvar' : 'Criar'"
          type="submit"
          class="fit q-mt-md"
          unelevated
          :loading="loading"
          text-color="dark"
          @click="save"
        />
        <q-btn
          v-if="transactionEdit?.code"
          color="red"
          label="Excluir"
          type="submit"
          class="fit q-mt-md"
          unelevated
          :loading="loading"
          text-color="white"
          @click="onDelete"
        />
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<style lang="sass">
.transaction
  &-type
    width: 100%
    height: 48px
    border-radius: 4px
    background-color: rgba(0, 0, 0, 0.05)
    border: 2px solid rgba(0, 0, 0, 0.05)
    display: flex
    flex-wrap: nowrap
    align-items: center
    font-size: 16px
    font-weight: 600
    padding: 8px 12px
    cursor: pointer
    text-align: center !important
    justify-content: center
    .q-icon
      margin-right: 8px
      font-size: 20px
    &-active
      border-color: var(--q-primary)
</style>