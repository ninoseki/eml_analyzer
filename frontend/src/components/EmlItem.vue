<script setup lang="ts">
import { type PropType } from 'vue'

import Attachments from '@/components/attachments/AttachmentsItem.vue'
import Bodies from '@/components/bodies/BodiesItem.vue'
import Headers from '@/components/headers/Headers.vue'
import type { EmlType } from '@/schemas'

defineProps({
  eml: {
    type: Object as PropType<EmlType>,
    required: true
  }
})
</script>

<template>
  <Headers :header="eml.header" />
  <Bodies :bodies="eml.bodies" v-if="eml.bodies.length > 0" />
  <Attachments :attachments="eml.attachments" v-if="eml.attachments.length > 0" />
</template>
