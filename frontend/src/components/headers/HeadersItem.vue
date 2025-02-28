<script setup lang="ts">
import { type PropType } from 'vue'

import BasicHeaders from '@/components/headers/BasicHeaders.vue'
import Hops from '@/components/headers/HopsItem.vue'
import OtherHeaders from '@/components/headers/OtherHeaders.vue'
import SecurityHeaders from '@/components/headers/SecurityHeaders.vue'
import XHeaders from '@/components/headers/XHeaders.vue'
import type { HeaderType } from '@/schemas'

defineProps({
  header: {
    type: Object as PropType<HeaderType>,
    required: true
  }
})
</script>

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
