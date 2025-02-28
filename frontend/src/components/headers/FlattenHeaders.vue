<script setup lang="ts">
import { computed, type PropType } from 'vue'

import type { HeaderItemType } from '@/schemas'

interface FlattenHeader {
  id: string
  key: string
  value: string | number
}

const props = defineProps({
  headers: {
    type: Array as PropType<HeaderItemType[]>,
    required: true
  }
})

const flattenHeaders = computed(() => {
  const headers: FlattenHeader[] = []
  let index = 0
  for (const header of props.headers) {
    const key = header.key
    const values = header.values
    for (const value of values) {
      index += 1
      headers.push({
        id: key + index.toString(),
        key: key,
        value: value
      })
    }
  }
  return headers
})
</script>

<template>
  <div class="table-container">
    <table class="table is-fullwidth is-completely-borderless" v-if="flattenHeaders.length > 0">
      <tbody>
        <tr v-for="header in flattenHeaders" :key="header.id">
          <th>{{ header.key }}</th>
          <td>{{ header.value }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
