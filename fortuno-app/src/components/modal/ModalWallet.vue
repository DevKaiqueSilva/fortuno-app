<script setup lang="ts">
import { Notify } from 'quasar'
import { useWalletStore } from 'src/stores/wallet'
import type { IWallet } from 'src/types/IWallet'
import { rules } from 'src/utils/rules'
import { ref } from 'vue'

const walletStore = useWalletStore()

const visible = defineModel<boolean>('visible', { default: false })

const refWalletForm = ref()
const wallet = ref<IWallet>({
  code: '',
  name: '',
  type: 'credit_card',
  creditCardLimit: 0,
  creditCardExpirationDay: 0,
  creditCardCloseDay: 0
})
const loading = ref(false)

const onShow = () => {
  if (visible.value) {
    wallet.value = {
      code: '',
      name: '',
      type: 'credit_card',
      creditCardLimit: 0,
      creditCardExpirationDay: 0,
      creditCardCloseDay: 0
    }
  }
}

const save = async () => {
  if (refWalletForm.value.validate()) {
    loading.value = true
    const saved = await walletStore.saveWallet(wallet.value)
    if (saved) {
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
</script>

<template>
  <q-dialog v-model="visible" @show="onShow">
    <q-card style="width: 450px">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">Nova conta</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>
      <q-card-section>
        <q-form ref="refWalletForm" @submit="save">
          <div class="row q-mb-lg">
            <div class="col-6 q-pr-sm">
              <div
                class="wallet-type"
                :class="{ 'wallet-type-active': wallet.type === 'credit_card' }"
                @click="wallet.type = 'credit_card'"
              >
                <q-icon name="wallet" />
                Cartão de crédito
              </div>
            </div>
            <div class="col-6 q-pl-sm">
              <div
                class="wallet-type"
                :class="{ 'wallet-type-active': wallet.type === 'bank' }"
                @click="wallet.type = 'bank'"
              >
                <q-icon name="account_balance" />
                Conta bancária
              </div>
            </div>
          </div>
          <q-input
            v-model="wallet.name"
            filled
            label="Nome"
            class="q-mb-md"
            :rules="[rules.required]"
            lazy-rules
            placeholder="Digite um nome para a conta"
          />
          <div v-if="wallet.type == 'credit_card'" class="row">
            <div class="col-6 q-pr-sm">
              <q-input
                v-model="wallet.creditCardExpirationDay"
                filled
                label="Vencimento da fatura"
                class="q-mb-md"
                :rules="[rules.required, rules.dayOfMonth]"
                lazy-rules
                type="number"
                max="28"
                min="1"
              />
            </div>
            <div class="col-6 q-pl-sm">
              <q-input
                v-model="wallet.creditCardCloseDay"
                filled
                label="Melhor dia"
                class="q-mb-md"
                :rules="[rules.required, rules.dayOfMonth]"
                lazy-rules
                type="number"
              />
            </div>
            <div class="col-12">
              <q-input
                v-model="wallet.creditCardLimit"
                filled
                label="Limite (R$)"
                mask="#,##"
                fill-mask="0"
                :rules="[rules.required]"
                lazy-rules
                class="q-mb-md"
                reverse-fill-mask
              />
            </div>
          </div>
        </q-form>
        <q-btn
          color="primary"
          label="Criar"
          type="submit"
          class="fit"
          unelevated
          :loading="loading"
          text-color="dark"
          @click="save"
        />
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<style lang="sass">
.wallet
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
    .q-icon
      margin-right: 8px
      font-size: 20px
    &-active
      border-color: var(--q-primary)
</style>
