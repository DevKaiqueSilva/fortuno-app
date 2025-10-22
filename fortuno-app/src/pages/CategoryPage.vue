<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { useCategoryStore } from 'src/stores/category'
import CategoryItem from 'src/components/CategoryItem.vue'
import ModalCategory from 'src/components/modal/ModalCategory.vue'
import type { ICategory } from 'src/types/ICategory'

const categoryStore = useCategoryStore()
const showCategoryModal = ref(false)
const categoryEdit = ref<ICategory | undefined>(undefined)

const handleCategoryModal = (category?: ICategory) => {
  categoryEdit.value = category ?? undefined
  showCategoryModal.value = true
}

onMounted(async () => {
  await categoryStore.fetchCategories()
})
</script>
<template>
  <q-page class="category-page items-center justify-evenly text-dark fit">
    <div class="text-subtitle1 text-weight-bold q-mb-md">Categorias</div>
    <category-item 
      v-for="(category, i) in categoryStore.getCategories"
      :key="`category-${i}`"
      :category="category" 
      class="q-mb-md"
      @edit="handleCategoryModal(category)"
    />
    <q-btn
      color="primary"
      label="Nova categoria"
      class="fit q-mt-sm"
      text-color="dark"
      @click="handleCategoryModal()"
    />
    <modal-category v-model:visible="showCategoryModal" :category-edit="categoryEdit" />
  </q-page>
</template>
