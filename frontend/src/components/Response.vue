<template>
  <div>
    <Verdicts :verdicts="response.verdicts" />
    <Eml :eml="response.eml" />
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue"

import Eml from "@/components/Eml.vue"
import Verdicts from "@/components/verdicts/Verdicts.vue"
import { Response } from "@/types"
export default defineComponent({
  name: "ResponseComponent",
  props: {
    response: {
      type: Object as PropType<Response>,
      required: true
    }
  },
  components: { Eml, Verdicts }
})
</script>
