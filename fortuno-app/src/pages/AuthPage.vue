<template>
  <q-page class="auth-page row items-center justify-evenly fit">
    <q-img
      src="../assets/logo-name.png"
      style="height: 100px; width: 260px; display: block; margin: auto"
      class="q-d-block"
    />
    <div class="text-left fit q-mt-md q-mb-md">
      <b class="text-h6">Seja bem vindo!</b>
      <br />
      <span class="text-subtitle1">Como deseja continuar?</span>
    </div>
    <q-btn
      color="primary"
      label="Acessar conta"
      class="fit q-mb-md"
      text-color="dark"
      @click="$router.push('/login')"
    />
    <q-btn
      color="transparent"
      flat
      label="Cadastre-se"
      class="fit text-underline"
      text-color="white"
      @click="$router.push('/register')"
    />
  </q-page>
</template>

<script setup lang="ts"></script>
