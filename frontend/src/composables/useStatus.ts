import { computed } from 'vue'

import { useStatusStore } from '@/store'

export function useStatus() {
  const store = useStatusStore()
  const status = computed(() => store.status)
  return {
    status
  }
}
