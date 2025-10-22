<script setup lang="ts">
import MenuFooter from 'src/components/MenuFooter.vue';
import HeaderResume from 'src/components/header/HeaderResume.vue';
import HeaderWallet from 'src/components/header/HeaderWallet.vue';
import { useAuthStore } from 'src/stores/auth';
import { onBeforeMount } from 'vue';
import { useRoute } from 'vue-router';

const authStore = useAuthStore()
const route = useRoute();

onBeforeMount(async () => {
  await authStore.fetchUser();
});
</script>

<template>
  <q-layout class="main-layout bg-dark" view="lHh Lpr lFf">
    <div class="fit q-pa-md">
      <q-img
        src="../assets/logo-icon.png"
        style="height: 90px; width: 100px; display: block; margin: auto"
      />
      <div style="max-width: 400px;margin: auto;">
        <header-wallet v-if="route.name == 'wallet-detail'" />
        <header-resume v-else />
      </div>
    </div>
    <q-card class="main-bg-card">
      <q-page-container class="fit">
        <router-view />
      </q-page-container>
    </q-card>
    <MenuFooter />
  </q-layout>
</template>

<style lang="sass">
.main-layout
  display: flex
  flex-direction: column
  & .q-page
    min-height: auto !important
  .main-bg-card
    display: flex
    flex-grow: 1
    background: white !important
    border-radius: 50px 50px 0px 0px
    padding: 24px
    color: white
    .q-page-container
      max-width: 400px !important
      margin: 0 auto
</style>
