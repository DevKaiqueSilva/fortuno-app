<script setup lang="ts">
import { Notify } from 'quasar';
import { useAuthStore } from 'src/stores/auth';
import { rules } from 'src/utils/rules';
import { onMounted, ref } from 'vue';

const authStore = useAuthStore()
const refProfileForm = ref()

const userInfo = ref({
  name: '',
  email: '',
  phone: '',
})

const saveProfile = async () => {
  const isValid = await refProfileForm.value.validate()
  if (!isValid) {
    Notify.create({
      type: 'negative',
      message: 'Verifique os campos obrigatórios'
    })
    return
  }
  const name = userInfo.value.name.split(' ')
  await authStore.saveProfile({
    firstName: name[0] ?? '',
    lastName: name[name.length - 1] ?? '',
    phone: userInfo.value.phone.replace(/([() -])/g, ''),
    email: authStore.user?.email ?? ''
  })
}

onMounted(() => {
  if (!authStore.user) return
  userInfo.value.name = authStore.user.firstName + ' ' + authStore.user.lastName
  userInfo.value.email = authStore.user.email
  userInfo.value.phone = authStore.user.phone
})
</script>

<template>
  <div class="text-center">
    <q-avatar
      size="120px"
      font-size="52px"
      color="grey"
      text-color="white"
      icon="person" 
      class="q-mb-lg"
    />
    <q-form ref="refProfileForm" @submit.prevent>
      <q-input
        v-model="userInfo.name"
        filled
        label="Nome"
        :rules="[rules.required, rules.lettersOnly]"
        placeholder="Digite seu nome"
        lazy-rules
      />
      <q-input
        v-model="userInfo.phone"
        filled
        label="Celular"
        :rules="[rules.required, rules.phone]"
        type="tel"
        mask="(##) #####-####"
        placeholder="Digite seu celular"
        lazy-rules
      />
      <q-input
        v-model="userInfo.email"
        filled
        label="E-mail"
        disable
        type="email"
        lazy-rules
      />
    </q-form>
    <q-btn
      color="primary"
      label="Salvar"
      class="fit q-mt-lg"
      text-color="dark"
      @click="saveProfile"
    />
  </div>
</template>