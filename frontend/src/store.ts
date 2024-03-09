import { defineStore } from 'pinia'

import { API } from '@/api'
import type { StatusType } from '@/schemas'

export const useStatusStore = defineStore('status', {
  state: (): StatusType => {
    return {}
  },
  actions: {
    async getStatus() {
      const status = await API.getStatus()
      this.$state = status
    }
  }
})
