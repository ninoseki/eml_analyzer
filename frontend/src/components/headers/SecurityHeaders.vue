<script setup lang="ts">
import { computed, type PropType } from 'vue'

import FlattenHeaders from '@/components/headers/FlattenHeaders.vue'
import { securityKeys } from '@/constants'
import type { HeaderItemType, HeaderType } from '@/schemas'

const props = defineProps({
  header: {
    type: Object as PropType<HeaderType>,
    required: true
  }
})
const securityHeaders = computed(() => {
  const header = props.header.header
  const items = securityKeys.map((key) => {
    if (key in header) {
      return { key: key, values: header[key] }
    }
  })
  return items.filter((x): x is HeaderItemType => x !== undefined)
})
</script>

<template>
  <div v-if="securityHeaders.length > 0">
    <h3 class="text-lg font-bold">Security headers</h3>
    <FlattenHeaders :headers="securityHeaders" />
  </div>
</template>
