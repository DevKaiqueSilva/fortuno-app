import { boot } from 'quasar/wrappers'
import axios, { type AxiosInstance } from 'axios'
import jwt_decode from 'jwt-decode'
import { Notify } from 'quasar'

const TOKEN_VARIABLE = 'fortuno_auth_token'
const REFRESH_TOKEN_VARIABLE = 'fortuno_refresh_token'

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance
  }
}

const api = axios.create({
  baseURL: process.env.API_URL ?? ''
})

const verifyTokenExpired = (token: string) => {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const decoded: any = jwt_decode(token)
  if (decoded && decoded.exp) {
    const expires_date = new Date(decoded.exp * 1000)
    if (expires_date >= new Date()) {
      return false
    }
  }
  return true
}
const refreshToken = async () => {
  let new_token = ''
  const token = localStorage.getItem(TOKEN_VARIABLE)
  const refresh_token = localStorage.getItem(REFRESH_TOKEN_VARIABLE)
  if (token && refresh_token) {
    try {
      const { status, data } = await api.post(
        '/user/refresh-token/',
        {
          refresh: refresh_token
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
      if (status == 200) {
        new_token = data.accessToken
        saveAuth(data.accessToken, data.refreshToken)
      }
    } catch {
      cleanAuth()
      autoLogout()
    }
  } else {
    cleanAuth()
    autoLogout()
  }
  return new_token
}

const autoLogout = () => {
  Notify.create({
    message: 'Sessão expirada. Acesse sua conta novamente.',
    type: 'negative',
    iconColor: 'white'
  })
  setTimeout(() => {
    window.location.href = '/login'
  }, 100)
}

const cleanAuth = () => {
  localStorage.removeItem(TOKEN_VARIABLE)
  localStorage.removeItem(REFRESH_TOKEN_VARIABLE)
}

const saveAuth = (token: string, refresh_token: string) => {
  localStorage.setItem(TOKEN_VARIABLE, token)
  localStorage.setItem(REFRESH_TOKEN_VARIABLE, refresh_token)
}

api.interceptors.request.use(
  async (config) => {
    const token = localStorage.getItem(TOKEN_VARIABLE)
    if (token) {
      const auth_routes = ['/login', '/register']
      if (
        verifyTokenExpired(token) &&
        auth_routes.filter((r: string) => config.url?.includes(r)).length == 0 &&
        config.url != '/user/refresh-token/'
      ) {
        const new_token = await refreshToken()
        if (new_token) {
          config.headers.Authorization = `Bearer ${new_token}`
        }
      } else {
        config.headers.Authorization = `Bearer ${token}`
      }
    }
    return config
  },
  (error) => {
    return error
  }
)

export default boot(({ app }) => {
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api
})

export { api, saveAuth, cleanAuth, autoLogout }
