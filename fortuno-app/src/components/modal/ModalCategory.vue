<script setup lang="ts">
import { Notify } from 'quasar'
import { useCategoryStore } from 'src/stores/category'
import type { ICategory } from 'src/types/ICategory'
import { rules } from 'src/utils/rules'
import { computed, ref } from 'vue'
import CategoryItem from '../CategoryItem.vue'

const categoryStore = useCategoryStore()

const visible = defineModel<boolean>('visible', { default: false })
const props = defineProps<{
  categoryEdit?: ICategory | undefined
}>()

const refCategoryForm = ref()
const category = ref<ICategory>({
  code: '',
  name: '',
  icon: '',
  color: '',
  defaultPlatform: false
})
const loading = ref(false)

const iconOptions = computed(() => [
  'restaurant', 'fastfood', 'local_dining', 'local_cafe', 'local_bar',
  'shopping_cart', 'shopping_bag', 'store', 'local_mall', 'local_grocery_store',
  'local_gas_station', 'directions_car', 'directions_bus', 'train', 'flight',
  'home', 'apartment', 'business', 'work', 'school',
  'local_hospital', 'medical_services', 'fitness_center', 'spa', 'sports_soccer',
  'movie', 'theater_comedy', 'music_note', 'videogame_asset', 'casino',
  'phone', 'wifi', 'computer', 'tv', 'headphones',
  'pets', 'child_care', 'family_restroom', 'elderly', 'accessible',
  'attach_money', 'credit_card', 'account_balance', 'savings', 'paid',
  'local_laundry_service', 'cleaning_services', 'plumbing', 'electrical_services', 'build',
  'beach_access', 'park', 'nature', 'local_florist', 'eco'
])

const onShow = () => {
  if (visible.value) {
    category.value = {
      code: props.categoryEdit?.code ?? '',
      name: props.categoryEdit?.name ?? '',
      icon: props.categoryEdit?.icon ?? '',
      color: props.categoryEdit?.color ?? '#E1E1E1',
      defaultPlatform: false
    }
  }
}

const save = async () => {
  if (refCategoryForm.value.validate()) {
    loading.value = true
    const saved = await categoryStore.saveCategory(category.value)
    if (saved) {
      visible.value = false
    }
    loading.value = false
  } else {
    Notify.create({
      type: 'negative',
      message: 'Verifique os campos obrigatórios'
    })
  }
}
</script>

<template>
  <q-dialog v-model="visible" @show="onShow">
    <q-card style="width: 450px">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">Nova conta</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>
      <q-card-section>
        <q-form ref="refCategoryForm" @submit="save">
          <q-input
            v-model="category.name"
            filled
            label="Nome"
            class="q-mb-md"
            :rules="[rules.required]"
            lazy-rules
            placeholder="Digite um nome para a categoria"
          />
          <q-input
            filled
            v-model="category.color"
            label="Cor"
            :rules="['anyColor']"
          >
            <template v-slot:append>
              <q-icon name="colorize" class="cursor-pointer">
                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                  <q-color v-model="category.color" />
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>
          <q-input
            filled
            v-model="category.icon"
            label="Ícone"
            class="q-mb-md"
            :rules="[rules.required]"
            lazy-rules
            readonly
          >
            <template v-slot:append>
              <q-icon :name="'category'" class="cursor-pointer">
                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                  <q-card class="q-pa-md" style="width: 300px">
                    <div class="text-subtitle2 q-mb-md">Escolha um ícone</div>
                    <div class="row q-col-gutter-sm">
                      <div 
                        v-for="icon in iconOptions"
                        :key="icon"
                        class="col-3"
                      >
                        <q-btn
                          :icon="icon"
                          flat
                          size="lg"
                          class="full-width q-pa-md"
                          :color="category.icon === icon ? 'primary' : 'grey'"
                          @click="category.icon = icon"
                        />
                      </div>
                    </div>
                    <q-btn v-close-popup label="Fechar" color="primary" flat class="full-width q-mt-md" />
                  </q-card>
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>
          <category-item v-if="category.name" class="q-mb-lg" :category="category" hide-action />
        </q-form>
        <q-btn
          color="primary"
          label="Criar"
          type="submit"
          class="fit"
          unelevated
          :loading="loading"
          text-color="dark"
          @click="save"
        />
      </q-card-section>
    </q-card>
  </q-dialog>
</template>