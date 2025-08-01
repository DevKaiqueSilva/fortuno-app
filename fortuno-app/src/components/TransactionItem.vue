<template>
  <div class="transaction-item row align-center">
    <div class="transaction-item-icon">
      <q-icon name="restaurant" size="16px" />
    </div>
    <div class="q-pl-sm">
      <div class="text-subtitle2">Restaurant</div>
      <div class="text-caption">R$ 100,00</div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style lang="sass">
.transaction-item
  &-icon
    background-color: #FFD5D5
    width: 40px
    height: 40px
    border-radius: 8px
    display: flex
    justify-content: center
    align-items: center
</style>
