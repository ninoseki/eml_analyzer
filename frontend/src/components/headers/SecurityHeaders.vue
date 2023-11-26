<template>
  <div class="table-container">
    <H3Component>Security headers</H3Component>
    <FlattenHeaders :headers="securityHeaders" />
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from "vue"

import FlattenHeaders from "@/components/headers/FlattenHeaders.vue"
import H3Component from "@/components/ui/h3.vue"
import { Header, HeaderItem, securityKeys } from "@/types"

export default defineComponent({
  name: "SecurityHeaders",
  props: {
    header: {
      type: Object as PropType<Header>,
      required: true
    }
  },
  components: { FlattenHeaders, H3Component },
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
