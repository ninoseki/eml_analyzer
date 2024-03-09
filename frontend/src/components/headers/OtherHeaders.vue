<template>
  <div class="block" v-if="otherHeaders.length > 0">
    <h3 class="is-size-5 has-text-weight-bold">Other headers</h3>
    <FlattenHeaders :headers="otherHeaders" />
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, type PropType } from 'vue'

import FlattenHeaders from '@/components/headers/FlattenHeaders.vue'
import { basicKeys, securityKeys } from '@/constants'
import type { HeaderItemType, HeaderType } from '@/schemas'

export default defineComponent({
  name: 'OtherHeaders',
  props: {
    header: {
      type: Object as PropType<HeaderType>,
      required: true
    }
  },
  components: { FlattenHeaders },
  setup(props) {
    const otherHeaders = computed(() => {
      const header = props.header.header
      const keys = Object.keys(header)
      const otherKeys = keys
        .filter((key) => !key.startsWith('x-'))
        .filter((key) => securityKeys.indexOf(key) == -1)
        .filter((key) => basicKeys.indexOf(key) == -1)

      const items = otherKeys.map((key) => {
        if (key in header) {
          return { key: key, values: header[key] }
        }
      })

      return items.filter((x): x is HeaderItemType => x !== undefined)
    })

    return { otherHeaders }
  }
})
</script>
@/constants
