import { boot } from 'quasar/wrappers'

export const formatDate = (date: string, type: string) => {
  if (!!type === false) {
    type = 'datetime'
  }
  if (date) {
    if (type === 'datetime') {
      return `${date.substring(0, 10).split('-').reverse().join('/')} ${date.substring(11, 16)}`
    } else if (type === 'time') {
      return date.substring(11, 16)
    } else if (type === 'short-date') {
      const dateSplitted: Array<string> = date.substring(0, 10).split('-').reverse()
      dateSplitted[2] = dateSplitted[2]?.substring(2, 4) ?? ''
      return dateSplitted.join('/')
    } else {
      return date.substring(0, 10).split('-').reverse().join('/')
    }
  } else {
    return date
  }
}

export const formatCoinBR = (value: number, type?: string) => {
  if (!type) type = 'decimal'
  const i = typeof value !== 'number'
  const finalValue = (value / (type == 'decimal' ? 100 : 1)).toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
  if (i) {
    return value
  } else {
    return `R$ ${finalValue}`
  }
}

export default boot(({ app }) => {
  app.config.globalProperties.$formatCoinBR = formatCoinBR
  app.config.globalProperties.$formatDate = formatDate
})
