export interface ICategory {
  code: string
  name: string
  icon: string
  color: string
  defaultPlatform: boolean
}

export interface ICategoryDashboard {
  code: string
  name: string
  icon: string
  color: string
  totalDebit: number
  totalCredit: number
}