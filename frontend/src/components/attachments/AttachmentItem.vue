<script setup lang="ts">
import type { AxiosError } from 'axios'
import fileSize from 'filesize.js'
import { computed, type PropType, ref } from 'vue'

import AttachmentDownloadButton from '@/components/attachments/AttachmentDownloadButton.vue'
import AttachmentSubmissionButton from '@/components/attachments/AttachmentSubmissionButton.vue'
import AttachmentSubmissionNotification from '@/components/attachments/AttachmentSubmissionNotification.vue'
import ErrorMessage from '@/components/ErrorMessage.vue'
import IndicatorButton from '@/components/IndicatorButton.vue'
import type { AttachmentType } from '@/schemas'
import { useStatusStore } from '@/store'
import { InQuest, VirusTotal } from '@/submitters'

const props = defineProps({
  attachment: {
    type: Object as PropType<AttachmentType>,
    required: true
  },
  index: {
    type: Number,
    required: true
  }
})

const store = useStatusStore()
const status = computed(() => {
  return store.$state
})

const error = ref<AxiosError>()
const referenceUrl = ref<string>()

const onDisposeError = () => {
  error.value = undefined
}

const onSetError = (newError: AxiosError) => {
  error.value = newError
}

const onSetReferenceUrl = (newReferenceUrl: string) => {
  referenceUrl.value = newReferenceUrl
}

const header = computed(() => {
  return `#${props.index + 1}`
})

const vt = new VirusTotal()
const inquest = new InQuest()
</script>

<template>
  <div class="block">
    <h3 class="is-size-5 has-text-weight-bold">{{ header }}</h3>
    <table class="table is-fullwidth is-completely-borderless">
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
          <td>{{ attachment.mimeType || 'N/A' }}</td>
        </tr>
        <tr>
          <th>SHA256</th>
          <td>
            <IndicatorButton :value="attachment.hash.sha256" />
          </td>
        </tr>
      </tbody>
    </table>
    <p class="is-clearfix">
      <span class="buttons is-pulled-right">
        <AttachmentSubmissionButton
          :attachment="attachment"
          :submitter="vt"
          @set-error="onSetError"
          @set-reference-url="onSetReferenceUrl"
          v-if="status.vt"
        />
        <AttachmentSubmissionButton
          :attachment="attachment"
          :submitter="inquest"
          @set-error="onSetError"
          @set-reference-url="onSetReferenceUrl"
          v-if="status.inquest"
        />
        <AttachmentDownloadButton :attachment="attachment" />
      </span>
    </p>
    <AttachmentSubmissionNotification
      class="mt-1"
      :referenceUrl="referenceUrl"
      v-if="referenceUrl"
    />
    <ErrorMessage
      class="mt-1"
      :error="error"
      :disposable="true"
      @dispose="onDisposeError"
      v-if="error"
    />
  </div>
</template>
