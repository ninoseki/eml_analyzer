<template>
  <div class="block" v-if="securityHeaders.length > 0">
    <h3 class="is-size-5 has-text-weight-bold">Security headers</h3>
    <FlattenHeaders :headers="securityHeaders" />
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, type PropType } from 'vue'

import FlattenHeaders from '@/components/headers/FlattenHeaders.vue'
import { securityKeys } from '@/constants'
import type { HeaderItemType, HeaderType } from '@/schemas'

export default defineComponent({
  name: 'SecurityHeaders',
  props: {
    header: {
      type: Object as PropType<HeaderType>,
      required: true
    }
  },
  components: { FlattenHeaders },
  setup(props) {
    const securityHeaders = computed(() => {
      const header = props.header.header
      const items = securityKeys.map((key) => {
        if (key in header) {
          return { key: key, values: header[key] }
        }
      })
      return items.filter((x): x is HeaderItemType => x !== undefined)
    })

    return { securityHeaders }
  }
})
</script>
@/constants
