<script lang="ts" setup>
import { useAuthStore } from 'src/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  setTimeout(() => {
    window.location.href = '/login'
  }, 100)
}
</script>

<template>
  <q-page class="transactions-page items-center justify-evenly text-dark fit">  
    <q-btn outline label="Minhas categorias" class="fit q-mb-md" @click="router.push('/categories')"/>
    <q-btn outline label="Meu perfil" class="fit q-mb-md" @click="router.push('/profile-info')" />
    <q-btn
      color="primary"
      label="Sair da conta"
      class="fit q-mt-sm"
      text-color="dark"
      @click="logout"
    />
  </q-page>
</template>
