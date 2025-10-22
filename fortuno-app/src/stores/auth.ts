import { defineStore } from 'pinia'
import { api, autoLogout, cleanAuth, saveAuth } from 'boot/axios'
import { Notify } from 'quasar'

interface ILoginPayload {
  email: string
  password: string
}

interface IRegisterPayload {
  email: string
  firstName: string
  lastName: string
  phone: string
  password: string
}

interface IUser {
  email: string
  firstName: string
  lastName: string
  phone: string
  balance?: {
    totalCredit: number
    totalDebit: number
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as IUser | null,
    token: localStorage.getItem('fortuno_auth_token') || ''
  }),
  actions: {
    async login(payload: ILoginPayload) {
      const { data } = await api.post('/api/user/login/', payload)
      this.token = data.token
      this.user = data
      saveAuth(data.accessToken, data.refresh_token)
    },
    async register(payload: IRegisterPayload) {
      let success = false
      try {
        const { status } = await api.post('/api/user/register/', payload)
        if (status === 200) {
          await this.login({
            email: payload.email,
            password: payload.password
          })
          success = true
        }
      } catch (error) {
        console.log(error)
        Notify.create({
          message: 'Falha ao criar conta',
          type: 'negative',
          iconColor: 'white'
        })
      }
      return success
    },
    async saveProfile(payload: IUser) {
      let success = false
      try {
        const { status } = await api.put('/api/user/', payload)
        if (status === 200) {
          success = true
          Notify.create({
            message: 'Perfil atualizado com sucesso',
            type: 'success',
            iconColor: 'white'
          })
        }
      } catch (error) {
        console.log(error)
        Notify.create({
          message: 'Falha ao salvar perfil',
          type: 'negative',
          iconColor: 'white'
        })
      }
      return success
    },
    async fetchUser() {
      try {
        const { data } = await api.get('/api/user/me')
        this.user = data
      } catch {
        cleanAuth()
        autoLogout()
      }
    },
    logout() {
      this.token = ''
      this.user = null
      cleanAuth()
    }
  }
})
