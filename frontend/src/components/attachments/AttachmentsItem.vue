<script setup lang="ts">
import { type PropType } from 'vue'

import Attachment from '@/components/attachments/AttachmentItem.vue'
import type { AttachmentType } from '@/schemas'

defineProps({
  attachments: {
    type: Array as PropType<AttachmentType[]>,
    required: true
  }
})
</script>

<template>
  <div class="block">
    <h2 class="is-size-4 has-text-weight-bold middle">Attachments</h2>
    <Attachment
      v-for="(attachment, index) in attachments"
      :key="attachment.hash.md5"
      :attachment="attachment"
      :index="index"
    />
  </div>
</template>
