<template>
  <q-footer bordered class="menu-footer bg-white text-primary">
    <q-tabs
      :model-value="tab"
      no-caps
      active-color="primary"
      indicator-color="transparent"
      class="text-grey-8"
    >
      <q-tab name="dashboard" icon="home" @click="$router.push('/')" />
      <q-tab name="transactions" icon="attach_money" @click="$router.push('/transactions')" />
      <q-tab>
        <q-btn
          icon="add"
          size="15px"
          padding="xs"
          color="primary"
          text-color="dark"
          style="width: 35px !important; height: 35px !important"
        />
      </q-tab>
      <q-tab name="wallet" icon="account_balance_wallet" @click="$router.push('/wallet')" />
      <q-tab name="profile" icon="account_circle" @click="$router.push('/profile')" />
    </q-tabs>
  </q-footer>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const tab = ref('');

onMounted(() => {
  if (route.name) {
    tab.value = route.name.toString();
    console.log(tab.value);
  }
});
</script>

<style lang="sass">
.menu-footer
  height: 55px
  .q-tabs
    height: 100%
    .q-tab__icon
      font-size: 28px
</style>
