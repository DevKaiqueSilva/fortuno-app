<script setup lang="ts">
import { rules } from 'src/utils/rules'
import { useAuthStore } from 'src/stores/auth'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const userInfo = ref({
  name: '',
  phone: '',
  email: '',
  password: ''
})

const showPassword = ref(false)
const registerForm = ref()
const loading = ref(false)

const passwordLevel = computed((): number => {
  let score = 0
  const password = userInfo.value.password

  // Basic requirements
  if (password.length >= 8) score += 2
  if (/[A-Z]/.test(password)) score += 2
  if (/[a-z]/.test(password)) score += 2
  if (/[0-9]/.test(password)) score += 2
  if (/[^A-Za-z0-9]/.test(password)) score += 2

  return Math.min(score, 10)
})

const register = async () => {
  const formIsValid = await registerForm.value.validate()
  if (!formIsValid) {
    return
  }
  loading.value = true
  const name = userInfo.value.name.split(' ')
  const success = await authStore.register({
    email: userInfo.value.email,
    password: userInfo.value.password,
    firstName: name[0] ?? '',
    lastName: name[name.length - 1] ?? '',
    phone: userInfo.value.phone.replace(/([() -])/g, '')
  })
  if (success) {
    await router.push('/')
  }
  setTimeout(() => {
    loading.value = false
  }, 1000)
}
</script>

<template>
  <q-page class="register-page row items-center justify-evenly fit">
    <q-btn
      flat
      round
      color="white"
      icon="arrow_back"
      class="absolute-top-left"
      @click="router.push('/')"
    />
    <q-img
      src="../assets/logo-icon.png"
      style="height: 150px; width: 150px; display: block; margin: auto"
    />
    <div class="fit q-mt-md q-mb-md">
      <b class="text-h6">Criar conta</b>
    </div>
    <q-form ref="registerForm" class="fit" @submit="register">
      <q-input
        v-model="userInfo.name"
        filled
        label="Nome"
        :rules="[rules.required, rules.lettersOnly]"
        dark
        class="q-mb-lg"
        placeholder="Digite seu nome"
        lazy-rules
      />
      <q-input
        v-model="userInfo.phone"
        filled
        label="Celular"
        :rules="[rules.required, rules.phone]"
        type="tel"
        mask="(##) #####-####"
        dark
        class="q-mb-lg"
        placeholder="Digite seu celular"
        lazy-rules
      />
      <q-input
        v-model="userInfo.email"
        filled
        label="E-mail"
        type="email"
        :rules="[rules.required, rules.email]"
        dark
        class="q-mb-lg"
        placeholder="Digite seu e-mail"
        lazy-rules
      />
      <q-input
        v-model="userInfo.password"
        filled
        label="Senha"
        :rules="[rules.required, rules.password]"
        dark
        :type="showPassword ? 'text' : 'password'"
        class="q-mb-md"
        placeholder="Digite sua senha"
        lazy-rules
      >
        <template v-slot:append>
          <q-icon
            :name="`visibility${!showPassword ? '_off' : ''}`"
            color="white"
            @click="showPassword = !showPassword"
          />
        </template>
      </q-input>
      <div class="row">
        <div class="q-pr-xs col-4">
          <q-card
            class="password-level"
            :style="`background-color: ${passwordLevel < 4 ? '#D9D9D9' : '#46AD4F'}`"
          />
        </div>
        <div class="q-px-xs col-4">
          <q-card
            class="password-level"
            :style="`background-color: ${passwordLevel < 8 ? '#D9D9D9' : '#46AD4F'}`"
          />
        </div>
        <div class="q-pl-xs col-4">
          <q-card
            class="password-level"
            :style="`background-color: ${passwordLevel < 10 ? '#D9D9D9' : '#46AD4F'}`"
          />
        </div>
      </div>
      <div class="q-mt-sm text-caption">
        A senha deve conter:
        <ol class="q-mt-none">
          <li>Mínimo de 8 caracteres</li>
          <li>
            Deve conter pelo menos:
            <ul>
              <li>1 letra maiúscula (A–Z)</li>
              <li>1 letra minúscula (a–z)</li>
              <li>1 número (0–9)</li>
              <li>1 símbolo (como @, #, $, %, etc.)</li>
            </ul>
          </li>
        </ol>
      </div>
    </q-form>
    <q-btn
      color="primary"
      label="Criar conta"
      class="fit q-mt-md"
      text-color="dark"
      :disable="loading"
      :loading="loading"
      @click="register"
    />
  </q-page>
</template>

<style lang="sass">
.register-page
  .password-level
    height: 10px
    border-radius: 8px
    background-color: #D9D9D9
</style>
