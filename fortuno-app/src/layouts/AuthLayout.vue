<template>
  <q-layout class="auth-layout" view="lHh Lpr lFf">
    <q-img src="../assets/welcome.svg" class="welcome-img" />
    <q-card class="auth-bg-card">
      <q-page-container class="fit" style="max-width: 400px; margin: 0 auto">
        <router-view />
      </q-page-container>
    </q-card>
  </q-layout>
</template>

<script setup lang="ts"></script>

<style lang="sass">
.welcome-img
  height: 45vh
  max-height: 350px
  width: 100%
  max-width: 300px
  display: block
  margin: auto
  transition: height 0.5s ease-in
.auth-layout
  display: flex
  flex-direction: column
  & .q-page
    min-height: auto !important
.auth-bg-card
  display: flex
  flex-grow: 1
  background: var(--q-dark)
  border-radius: 50px 50px 0px 0px
  padding: 24px
  color: white

.auth-layout:has(.login-page), .auth-layout:has(.register-page)
  .welcome-img
    height: 0px !important
    transition: height 0.5s ease-in
  .auth-bg-card
    border-radius: 0px
    transition: 0.6s ease-in
</style>
