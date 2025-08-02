<script setup lang="ts">
import { computed, type PropType } from 'vue'

import FlattenHeaders from '@/components/headers/FlattenHeaders.vue'
import type { HeaderItemType, HeaderType } from '@/schemas'

const props = defineProps({
  header: {
    type: Object as PropType<HeaderType>,
    required: true
  }
})

const xHeaders = computed(() => {
  const header = props.header.header
  const keys = Object.keys(header)
  const xKeys = keys.filter((key) => key.startsWith('x-'))

  const items = xKeys.map((key) => {
    if (key in header) {
      return { key: key, values: header[key] }
    }
  })

  return items.filter((x): x is HeaderItemType => x !== undefined)
})
</script>

<template>
  <div v-if="xHeaders.length > 0">
    <h3 class="text-lg font-bold">X headers</h3>
    <FlattenHeaders :headers="xHeaders" />
  </div>
</template>
