<script setup lang="ts">
import MenuFooter from 'src/components/MenuFooter.vue';
</script>

<template>
  <q-layout class="main-layout bg-dark" view="lHh Lpr lFf">
    <div class="fit q-pa-md">
      <q-img
        src="../assets/logo-icon.png"
        style="height: 90px; width: 100px; display: block; margin: auto"
      />
      <div class="text-center text-h5 text-weight-bold text-white q-mt-xs q-mb-sm">R$ 25898,00</div>
      <div class="row text-subtitle1">
        <div class="col-6 text-green text-right q-pr-sm" style="border-right: 1px solid white">
          <q-icon name="arrow_upward_alt" color="green" class="inline-block" />
          R$2000,00
        </div>
        <div class="col-6 text-red text-left q-pl-sm">
          R$2000,00
          <q-icon name="arrow_downward_alt" color="red" size="30" class="inline-block" />
        </div>
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
