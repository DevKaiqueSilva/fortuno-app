<script setup lang="ts">
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth'
import { rules } from 'src/utils/rules'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const $q = useQuasar()

const authStore = useAuthStore()
const router = useRouter()

const userInfo = ref({
  email: '',
  password: ''
})
const loginForm = ref()

const showPassword = ref(false)

const onSubmit = async () => {
  try {
    const formIsValid = await loginForm.value.validate()
    if (!formIsValid) {
      return
    }
    await authStore.login({
      email: userInfo.value.email,
      password: userInfo.value.password
    })
    if (authStore.user) {
      await router.push('/')
    }
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (err: any) {
    const responseStatus = err?.response?.status ?? 400
    $q.notify({
      color: 'red',
      textColor: 'white',
      icon: 'warning',
      message: responseStatus == 401 ? 'E-mail e/ou senha inválidos' : 'Falha ao acessar a conta'
    })
  }
}
</script>

<template>
  <q-page class="login-page row items-center justify-evenly fit">
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
      style="height: 200px; width: 200px; display: block; margin: auto"
    />
    <div class="fit q-mt-md q-mb-md">
      <b class="text-h6">Acesse sua conta</b>
    </div>
    <q-form ref="loginForm" @submit="onSubmit" class="fit">
      <div>
        <q-input
          v-model="userInfo.email"
          filled
          type="email"
          label="E-mail"
          dark
          class="q-mb-lg"
          :rules="[rules.required, rules.email]"
          placeholder="Digite seu e-mail"
          lazy-rules
        />
        <q-input
          v-model="userInfo.password"
          filled
          label="Senha"
          dark
          :type="showPassword ? 'text' : 'password'"
          class="q-mb-md"
          :rules="[rules.required]"
          lazy-rules
          placeholder="Digite sua senha"
        >
          <template v-slot:append>
            <q-icon
              :name="`visibility${!showPassword ? '_off' : ''}`"
              color="white"
              @click="showPassword = !showPassword"
            />
          </template>
        </q-input>
        <div class="text-right fit">
          <a class="white-text" @click="router.push('/recovery-password')">Esqueci a senha</a>
        </div>
      </div>
      <q-btn color="primary" label="Acessar" class="fit q-mt-xl" text-color="dark" type="submit" />
    </q-form>
  </q-page>
</template>
