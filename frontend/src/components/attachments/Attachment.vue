<template>
  <div>
    <nav class="navbar">
      <div class="navbar-brand">
        <h3 class="is-size-5 has-text-weight-bold">
          {{ header }}
        </h3>
      </div>
      <div class="navbar-menu">
        <div class="navbar-end">
          <Submitters :type="sha256Type" :value="attachment" />
          <div class="navbar-item">
            <button class="button" @click="confirmDownload">
              <span class="icon"><i class="fas fa-download"></i></span>
              <span>Download</span>
            </button>
          </div>
        </div>
      </div>
    </nav>
    <div class="table-container">
      <table class="table is-fullwidth">
        <tbody>
          <tr>
            <th>Filename</th>
            <td>{{ attachment.filename }}</td>
          </tr>
          <tr>
            <th>Size</th>
            <td>{{ fileSize(attachment.size) }}</td>
          </tr>
          <tr>
            <th>MIME type</th>
            <td>{{ attachment.mimeType || "N/A" }}</td>
          </tr>
          <tr>
            <th>Hash</th>
            <td>
              <Indicators :type="sha256Type" v-bind:values="values" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import fileSize from "filesize.js"
import fileDownload from "js-file-download"
import Vue from "vue"
import { computed, defineComponent, PropType } from "vue"

import Indicators from "@/components/indicators/Indicators.vue"
import Submitters from "@/components/submitters/Submitters.vue"
import { Attachment, SubmitType } from "@/types"
import { b64toBlob } from "@/utils/base64"

export default defineComponent({
  name: "AttachmentComponent",
  props: {
    attachment: {
      type: Object as PropType<Attachment>,
      required: true
    },
    index: {
      type: Number,
      required: true
    }
  },
  components: { Submitters, Indicators },
  setup(props) {
    const buefy = Vue.prototype.$buefy

    const header = computed(() => {
      return `#${props.index + 1}`
    })
    const values = computed(() => {
      return [props.attachment.hash.sha256]
    })
    const sha256Type: SubmitType = "sha256"

    const download = () => {
      const decoded = b64toBlob(props.attachment.raw)
      fileDownload(decoded, props.attachment.filename, props.attachment.mimeTypeShort)
    }

    const confirmDownload = () => {
      buefy.dialog.confirm({
        message: `Are you sure to download this attachment? (filename: ${props.attachment.filename})?`,
        onConfirm: () => download()
      })
    }

    return { header, values, sha256Type, fileSize, confirmDownload }
  }
})
</script>
