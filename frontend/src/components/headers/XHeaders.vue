<template>
  <div class="block" v-if="xHeaders.length > 0">
    <h3 class="is-size-5 has-text-weight-bold">X headers</h3>
    <FlattenHeaders :headers="xHeaders" />
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, type PropType } from 'vue'

import FlattenHeaders from '@/components/headers/FlattenHeaders.vue'
import type { HeaderItemType, HeaderType } from '@/schemas'

export default defineComponent({
  name: 'XHeaders',
  props: {
    header: {
      type: Object as PropType<HeaderType>,
      required: true
    }
  },
  components: { FlattenHeaders },
  setup(props) {
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

    return { xHeaders }
  }
})
</script>
