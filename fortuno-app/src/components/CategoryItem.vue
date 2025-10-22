<script setup lang="ts">
import { useQuasar } from 'quasar';
import { useCategoryStore } from 'src/stores/category';
import type { ICategory } from 'src/types/ICategory';

const props = defineProps<{
  category: ICategory
  hideAction?: boolean 
}>()

const emit = defineEmits(['edit'])
const $q = useQuasar()
const categoryStore = useCategoryStore()

const onDelete = () => {
  $q.dialog({
    title: 'Confirmar exclusão',
    message: 'Deseja excluir a categoria?',
    cancel: {
      label: 'Cancelar',
      color: 'grey',
      flat: true
    },
    ok: {
      label: 'Excluir',
      color: 'negative'
    }
  }).onOk(() => {
    void categoryStore.deleteCategory(props.category.code)
  })
}
</script>
<template>
  <div class="transaction-item row items-center">
    <div class="transaction-item-icon" :style="{ backgroundColor: category.color }">
      <q-icon v-if="category.icon" :name="category.icon" size="16px" />
      <div v-else>-</div>
    </div>
    <div class="q-pl-sm fit">
      <div class="text-subtitle2">{{ category.name }}
        <span v-if="category.defaultPlatform">(Padrão)</span>
      </div>
    </div>
    <q-icon 
      v-if="!category.defaultPlatform && !hideAction"
      name="edit"
      size="20px"
      class="q-mx-sm cursor-pointer"
      @click="emit('edit')"
    />
    <q-icon
      v-if="!category.defaultPlatform && !hideAction" 
      name="delete"
      size="20px"
      class="q-ml-sm cursor-pointer" 
      @click="onDelete"
    />
  </div>
</template>

<style lang="sass">
.transaction-item
  flex-wrap: nowrap
  &-icon
    min-width: 40px
    width: 40px
    height: 40px
    border-radius: 8px
    display: flex
    justify-content: center
    align-items: center
</style>
