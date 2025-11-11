import { defineStore } from 'pinia'

import { API } from '@/api'
import type { StatusType } from '@/schemas'

export const useStatusStore = defineStore('status', {
  state: () => {
    return { status: {} as StatusType }
  },
  actions: {
    async initialize() {
      this.status = await API.getStatus()
    }
  }
})

export const initializeStores = async () => {
  const statusStore = useStatusStore()
  await statusStore.initialize()
}
