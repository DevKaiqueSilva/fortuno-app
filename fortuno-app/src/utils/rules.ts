export const rules = {
  required: (v: string) => !!v || 'Campo obrigatório',
  date: (v: string) => (!!v && v.length == 10) || 'Data inválida',
  email: (value: string) => {
    const pattern =
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    return pattern.test(value) || 'E-mail invalido'
  },
  phone: (v: string) => (!!v && (v.length == 14 || v.length == 15)) || 'Telefone inválido',
  lettersOnly: (v: string) => /^[a-zA-ZÀ-ÿ\s'-]*$/.test(v) || 'Somente letras e espaços',
  password: (v: string) => {
    if (v.length < 8) return 'Mínimo de 8 caracteres'
    if (!/[A-Z]/.test(v)) return 'Deve conter pelo menos 1 letra maiúscula'
    if (!/[a-z]/.test(v)) return 'Deve conter pelo menos 1 letra minúscula'
    if (!/[0-9]/.test(v)) return 'Deve conter pelo menos 1 número'
    if (!/[^A-Za-z0-9]/.test(v)) return 'Deve conter pelo menos 1 símbolo'
    return true
  },
  dayOfMonth: (v: string) => (!!v && parseInt(v) > 0 && parseInt(v) <= 31) || 'Dia inválido'
}
