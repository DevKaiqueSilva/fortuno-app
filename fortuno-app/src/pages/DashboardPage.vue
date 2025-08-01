<template>
  <q-page class="dashboard-page items-center justify-evenly text-dark fit">
    <div class="q-mb-md">
      <div class="text-subtitle1 text-weight-bold">Contas</div>
      <div class="row">
        <q-card class="dashboard-account">
          <span class="text-weight-medium">Nubank</span>
          <div class="text-right">R$ 100,00</div>
        </q-card>
      </div>
    </div>
    <div class="q-mb-md">
      <div class="text-subtitle1 text-weight-bold">Gastos por categoria</div>
      <div id="chart">
        <ApexChart type="pie" width="380" :options="chartOptions" :series="series"></ApexChart>
      </div>
    </div>
    <div>
      <div class="text-subtitle1 text-weight-bold q-mb-xs">Últimas transações</div>
      <TransactionItem />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import TransactionItem from 'src/components/TransactionItem.vue';
import ApexChart from 'vue3-apexcharts';
import { ref } from 'vue';

const series = ref([44, 55, 13, 43, 22]);
const chartOptions = ref({
  chart: {
    width: 380,
    type: 'pie',
  },
  labels: ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'],
  responsive: [
    {
      breakpoint: 480,
      options: {
        chart: {
          width: '90%',
        },
        legend: {
          position: 'right',
        },
      },
    },
  ],
});
</script>

<style lang="sass">
.dashboard
  &-account
    background: #9EA4AE !important
    border-radius: 8px
    padding: 8px
    box-shadow: none
</style>
