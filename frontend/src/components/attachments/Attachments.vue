<template>
  <div class="block">
    <h2 class="is-size-4 has-text-weight-bold middle">Attachments</h2>
    <AttachmentComponent
      v-for="(attachment, index) in attachments"
      :key="attachment.hash.md5"
      :attachment="attachment"
      :index="index"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

import AttachmentComponent from '@/components/attachments/Attachment.vue'
import type { Attachment } from '@/types'

export default defineComponent({
  name: 'AttachmentsComponent',
  props: {
    attachments: {
      type: Array as PropType<Attachment[]>,
      required: true
    }
  },
  components: { AttachmentComponent },
  setup() {}
})
</script>
