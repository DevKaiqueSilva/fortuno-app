<script lang="ts" setup>
import { formatCoinBR } from 'src/boot/format'
import { useCategoryStore } from 'src/stores/category'
import { computed, onMounted } from 'vue'
import ApexChart from 'vue3-apexcharts'

const categoryStore = useCategoryStore()

const series = computed(() => categoryStore.categoriesDashboard.map(item => item.totalDebit))
const chartOptions = computed( () => ({
  chart: {
    width: 380,
    type: 'pie'
  },
  labels: categoryStore.categoriesDashboard.map(item => item.name),
  colors: categoryStore.categoriesDashboard.map(item => item.color),
  tooltip: {
    y: {
      formatter: (value: number) => formatCoinBR(value)
    }
  },
  responsive: [
    {
      breakpoint: 480,
      options: {
        chart: {
          width: '90%'
        },
        legend: {
          position: 'right'
        }
      }
    }
  ]
}))

onMounted(async () => {
  await categoryStore.fetchCategoriesDashboard()
})
</script>

<template>
  <div class="q-mb-md">
    <div class="text-subtitle1 text-weight-bold">Gastos por categoria</div>
    <div id="chart">
      <ApexChart 
        v-if="series.length > 0"
        type="pie"
        width="380"
        :options="chartOptions"
        :series="series"
        class="q-mt-md"
      />
      <div v-else class="q-my-md text-center">Sem dados</div>
    </div>
  </div>
</template>