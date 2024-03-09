<template>
  <div class="block">
    <h2 class="is-size-4 has-text-weight-bold middle">Headers</h2>
    <BasicHeaders :header="header" />
    <Hops :header="header" />
    <SecurityHeaders :header="header" />
    <XHeaders :header="header" />
    <OtherHeaders :header="header" />
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

import BasicHeaders from '@/components/headers/BasicHeaders.vue'
import Hops from '@/components/headers/Hops.vue'
import OtherHeaders from '@/components/headers/OtherHeaders.vue'
import SecurityHeaders from '@/components/headers/SecurityHeaders.vue'
import XHeaders from '@/components/headers/XHeaders.vue'
import type { HeaderType } from '@/schemas'

export default defineComponent({
  name: 'HeadersComponent',
  props: {
    header: {
      type: Object as PropType<HeaderType>,
      required: true
    }
  },
  components: {
    BasicHeaders,
    Hops,
    OtherHeaders,
    SecurityHeaders,
    XHeaders
  }
})
</script>
