<script setup lang="ts">
import fileDownload from 'js-file-download'
import { type PropType } from 'vue'

import type { AttachmentType } from '@/schemas'
import { b64toBlob } from '@/utils'

const props = defineProps({
  attachment: {
    type: Object as PropType<AttachmentType>,
    required: true
  }
})

const download = () => {
  const decoded = b64toBlob(props.attachment.raw)
  fileDownload(decoded, props.attachment.filename, props.attachment.mimeTypeShort)
}

const confirm = () => {
  const confirmed = window.confirm(
    `Are you sure to download this attachment? (filename: ${props.attachment.filename})?`
  )
  if (confirmed) {
    download()
  }
}
</script>

<template>
  <span class="button is-light" @click="confirm">
    <span class="icon">
      <font-awesome-icon icon="download"></font-awesome-icon>
    </span>
    <span>Download</span>
  </span>
</template>
