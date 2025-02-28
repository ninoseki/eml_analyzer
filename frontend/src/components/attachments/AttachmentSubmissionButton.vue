<script setup lang="ts">
import axios from 'axios'
import { type PropType } from 'vue'
import { useAsyncTask } from 'vue-concurrency'

import type { AttachmentType, SubmissionResultType, SubmitterType } from '@/schemas'

const props = defineProps({
  attachment: {
    type: Object as PropType<AttachmentType>,
    required: true
  },
  submitter: {
    type: Object as PropType<SubmitterType>,
    required: true
  }
})
const emits = defineEmits(['set-reference-url', 'set-error'])

const submitTask = useAsyncTask<SubmissionResultType, []>(async () => {
  return await props.submitter.submit(props.attachment)
})

const submit = async () => {
  try {
    const result = await submitTask.perform()
    emits('set-reference-url', result.referenceUrl)
  } catch (err) {
    if (axios.isAxiosError(err)) {
      emits('set-error', err)
    }
  }
}

const confirm = () => {
  const confirmed = window.confirm(
    `Are you sure to submit this attachment to ${props.submitter.name}?`
  )
  if (confirmed) {
    submit()
  }
}
</script>

<template>
  <span class="button is-light" @click="confirm">
    <span class="icon">
      <font-awesome-icon icon="spinner" spin v-if="submitTask.isRunning"></font-awesome-icon>
      <font-awesome-icon icon="upload" v-else></font-awesome-icon>
    </span>
    <span>{{ submitter.name }}</span>
  </span>
</template>
