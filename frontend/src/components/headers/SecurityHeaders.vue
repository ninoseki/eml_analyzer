<template>
  <div class="block" v-if="securityHeaders.length > 0">
    <h3 class="is-size-5 has-text-weight-bold">Security headers</h3>
    <FlattenHeaders :headers="securityHeaders" />
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, type PropType } from 'vue'

import FlattenHeaders from '@/components/headers/FlattenHeaders.vue'
import { type Header, type HeaderItem, securityKeys } from '@/types'

export default defineComponent({
  name: 'SecurityHeaders',
  props: {
    header: {
      type: Object as PropType<Header>,
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
      return items.filter((x): x is HeaderItem => x !== undefined)
    })

    return { securityHeaders }
  }
})
</script>
