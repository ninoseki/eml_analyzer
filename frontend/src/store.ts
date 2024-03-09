import { defineStore } from 'pinia'

import { API } from '@/api'
import type { Status } from '@/types'

export const useStatusStore = defineStore('status', {
  state: (): Status => {
    return {}
  },
  actions: {
    async getStatus() {
      const status = await API.getStatus()
      this.$state = status
    }
  }
})
