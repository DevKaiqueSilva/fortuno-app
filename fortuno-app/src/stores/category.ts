import { defineStore } from 'pinia'
import { api } from 'boot/axios'
import type { ICategory, ICategoryDashboard } from 'src/types/ICategory'

export const useCategoryStore = defineStore('category', {
  state: () => ({
    categories: [] as Array<ICategory>,
    categoriesDashboard: [] as Array<ICategoryDashboard>
  }),
  getters: {
    getCategories(state) {
      return state.categories
    }
  },
  actions: {
    async fetchCategories(save: boolean = true) {
      let categories = [] as Array<ICategory>
      const { data, status } = await api.get('/api/category/?page_size=50')
      if (status === 200) {
        categories = data.results
        if (save) {
          this.categories = categories
        } 
      }
      return categories
    },
    async saveCategory(category: ICategory) {
      let saved = false
      const url = `/api/category/${category.code ? `${category.code}/` : ''}`
      const payload =  {
        name: category.name,
        icon: category.icon,
        color: category.color
      }
      const { status } = await (category.code ? api.put(url, payload) : api.post(url, payload))
      if ([200, 201].includes(status)) {
        saved = true
        await this.fetchCategories()
      }
      return saved
    },
    async deleteCategory(categoryCode: string) {
      let deleted = false
      const url = `/api/category/${categoryCode}/`
      const { status } = await api.delete(url)
      if (status === 204) {
        deleted = true
        await this.fetchCategories()
      }
      return deleted
    },
    async fetchCategoriesDashboard() {
      const { data, status } = await api.get('/api/category/dashboard/')
      if (status === 200) {
        this.categoriesDashboard = data
      }
    }
  }
})
