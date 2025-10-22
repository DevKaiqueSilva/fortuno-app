<script setup lang="ts">
import { formatCoinBR } from 'src/boot/format';
import { useAuthStore } from 'src/stores/auth';
import { computed } from 'vue';

const authStore = useAuthStore()

const user = computed(() => authStore.user)
</script>
<template>
  <div>
    <div class="text-center text-h5 text-weight-bold text-white q-mt-xs q-mb-sm">R$ 25898,00</div>
    <div class="row text-subtitle1">
      <div class="col-6 text-green text-right q-pr-sm" style="border-right: 1px solid white">
        <q-icon name="arrow_upward_alt" color="green" class="inline-block" />
        {{ formatCoinBR(user?.balance?.totalCredit ?? 0) }}
      </div>
      <div class="col-6 text-red text-left q-pl-sm">
         {{ formatCoinBR(user?.balance?.totalDebit ?? 0) }}
        <q-icon name="arrow_downward_alt" color="red" size="30" class="inline-block" />
      </div>
    </div>
  </div>
</template>