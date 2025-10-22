<script setup lang="ts">
import { ref, computed } from 'vue'

const emit = defineEmits<{
  change: [month: number, year: number]
}>()

const months = [
  'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

const currentDate = new Date()
const currentMonthIndex = ref(currentDate.getMonth())
const currentYear = ref(currentDate.getFullYear())

const displayText = computed(() => {
  const yearShort = currentYear.value.toString().slice(-2)
  return `${months[currentMonthIndex.value]}/${yearShort}`
})

const previousMonth = () => {
  if (currentMonthIndex.value === 0) {
    currentMonthIndex.value = 11
    currentYear.value--
  } else {
    currentMonthIndex.value--
  }
  emit('change', currentMonthIndex.value + 1, currentYear.value)
}

const nextMonth = () => {
  if (currentMonthIndex.value === 11) {
    currentMonthIndex.value = 0
    currentYear.value++
  } else {
    currentMonthIndex.value++
  }
  emit('change', currentMonthIndex.value + 1, currentYear.value)
}
</script>

<template>
  <div class="filter-month row align-center">
    <div class="col-2">
      <q-icon name="chevron_left" class="filter-month-button" size="24px" @click="previousMonth" />
    </div>
    <div class="col-8 text-center text-subtitle1 text-weight-bold">
      {{ displayText }}
    </div>
    <div class="col-2 d-flex text-right">
      <q-icon name="chevron_right" class="filter-month-button" size="24px" @click="nextMonth" />
    </div>
  </div>
</template>

<style lang="sass">
.filter-month
  &-button
    cursor: pointer
    &:hover
      border-radius: 100px
      background-color: #e1e1e1
</style>