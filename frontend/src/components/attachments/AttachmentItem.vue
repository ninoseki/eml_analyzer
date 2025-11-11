<script setup lang="ts">
import type { AxiosError } from 'axios'
import fileSize from 'filesize.js'
import { type PropType, ref } from 'vue'

import AttachmentDownloadButton from '@/components/attachments/AttachmentDownloadButton.vue'
import AttachmentSubmissionButton from '@/components/attachments/AttachmentSubmissionButton.vue'
import AttachmentSubmissionNotification from '@/components/attachments/AttachmentSubmissionNotification.vue'
import ErrorMessage from '@/components/ErrorMessage.vue'
import IndicatorButton from '@/components/IndicatorButton.vue'
import { useStatus } from '@/composables/useStatus'
import type { AttachmentType } from '@/schemas'
import { InQuest, VirusTotal } from '@/submitters'

defineProps({
  attachment: {
    type: Object as PropType<AttachmentType>,
    required: true
  }
})

const { status } = useStatus()
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

const vt = new VirusTotal()
const inquest = new InQuest()
</script>

<template>
  <table class="table w-full break-all">
    <tbody>
      <tr>
        <th class="w-80">Filename</th>
        <td>{{ attachment.filename }}</td>
      </tr>
      <tr>
        <th class="w-80">Size</th>
        <td>{{ fileSize(attachment.size) }}</td>
      </tr>
      <tr>
        <th class="w-80">MIME type</th>
        <td>{{ attachment.mimeType || 'N/A' }}</td>
      </tr>
      <tr>
        <th class="w-80">CID</th>
        <td>{{ attachment.contentId || 'N/A' }}</td>
      </tr>
      <tr>
        <th class="w-80">SHA256</th>
        <td>
          <IndicatorButton :value="attachment.hash.sha256" />
        </td>
      </tr>
    </tbody>
  </table>
  <div class="flex justify-end mt-4">
    <div class="flex gap-2">
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
    </div>
  </div>
  <AttachmentSubmissionNotification class="mt-1" :referenceUrl="referenceUrl" v-if="referenceUrl" />
  <ErrorMessage
    class="mt-1"
    :error="error"
    :disposable="true"
    @dispose="onDisposeError"
    v-if="error"
  />
</template>
