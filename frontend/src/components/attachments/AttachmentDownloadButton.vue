<template>
  <span class="button is-light" @click="confirm">
    <span class="icon">
      <font-awesome-icon icon="download"></font-awesome-icon>
    </span>
    <span>Download</span>
  </span>
</template>

<script lang="ts">
import fileDownload from 'js-file-download'
import { defineComponent, type PropType } from 'vue'

import type { Attachment } from '@/types'
import { b64toBlob } from '@/utils'

export default defineComponent({
  name: 'AttachmentDownloadButton',
  props: {
    attachment: {
      type: Object as PropType<Attachment>,
      required: true
    }
  },
  setup(props) {
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

    return { confirm }
  }
})
</script>
