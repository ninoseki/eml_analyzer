<script setup lang="ts">
import { type PropType } from 'vue'

import Attachments from '@/components/attachments/AttachmentsItem.vue'
import Bodies from '@/components/bodies/BodiesItem.vue'
import Headers from '@/components/headers/HeadersItem.vue'
import type { EmlType } from '@/schemas'

defineProps({
  eml: {
    type: Object as PropType<EmlType>,
    required: true
  }
})
</script>

<template>
  <Headers class="grid gap-4" :header="eml.header" />
  <Bodies
    class="grid gap-4"
    :bodies="eml.bodies"
    :attachments="eml.attachments"
    v-if="eml.bodies.length > 0"
  />
  <Attachments
    class="grid gap-4"
    :attachments="eml.attachments"
    v-if="eml.attachments.length > 0"
  />
</template>
