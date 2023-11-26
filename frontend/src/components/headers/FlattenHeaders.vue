<template>
  <table class="table is-fullwidth" v-if="hasFlattenHeaders">
    <tbody>
      <tr v-for="header in flattenHeaders" :key="header.id">
        <th>{{ header.key }}</th>
        <td>{{ header.value }}</td>
      </tr>
    </tbody>
  </table>
  <div v-else>
    <p>N/A</p>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from "vue"

import { HeaderItem } from "@/types"

interface FlattenHeader {
  id: string
  key: string
  value: string | number
}

export default defineComponent({
  name: "FlattenHeaders",
  props: {
    headers: {
      type: Array as PropType<HeaderItem[]>,
      required: true
    }
  },
  setup(props) {
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

    const hasFlattenHeaders = computed(() => {
      return flattenHeaders.value.length > 0
    })

    return { hasFlattenHeaders, flattenHeaders }
  }
})
</script>
