<template>
  <q-page class="login-page row items-center justify-evenly fit">
    <q-btn
      flat
      round
      color="white"
      icon="arrow_back"
      class="absolute-top-left"
      @click="$router.push('/')"
    />
    <q-img
      src="../assets/logo-icon.png"
      style="height: 200px; width: 200px; display: block; margin: auto"
    />
    <div class="fit q-mt-md q-mb-md">
      <b class="text-h6">Acesse sua conta</b>
    </div>
    <div class="fit">
      <q-input
        v-model="userInfo.email"
        filled
        type="email"
        label="E-mail"
        dark
        class="q-mb-lg"
        placeholder="Digite seu e-mail"
      />
      <q-input
        v-model="userInfo.password"
        filled
        label="Senha"
        dark
        :type="showPassword ? 'text' : 'password'"
        class="q-mb-md"
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
        <a class="white-text" @click="$router.push('/recovery-password')">Esqueci a senha</a>
      </div>
    </div>
    <q-btn color="primary" label="Acessar" class="fit q-mt-xl" text-color="dark" />
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const userInfo = ref({
  email: '',
  password: '',
});

const showPassword = ref(false);
</script>
