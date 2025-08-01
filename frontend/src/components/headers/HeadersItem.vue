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
  <h2 class="text-2xl font-bold middle">Headers</h2>
  <Hops :header="header" />
  <BasicHeaders :header="header" />
  <SecurityHeaders :header="header" />
  <XHeaders :header="header" />
  <OtherHeaders :header="header" />
</template>
