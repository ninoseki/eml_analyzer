<template>
  <span class="button is-light" @click="confirm">
    <span class="icon">
      <font-awesome-icon icon="spinner" spin v-if="submitTask.isRunning"></font-awesome-icon>
      <font-awesome-icon icon="upload" v-else></font-awesome-icon>
    </span>
    <span>{{ submitter.name }}</span>
  </span>
</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent, type PropType } from 'vue'
import { useAsyncTask } from 'vue-concurrency'

import type { AttachmentType, SubmissionResultType, SubmitterType } from '@/schemas'

export default defineComponent({
  name: 'AttachmentSubmissionButton',
  props: {
    attachment: {
      type: Object as PropType<AttachmentType>,
      required: true
    },
    submitter: {
      type: Object as PropType<SubmitterType>,
      required: true
    }
  },
  emits: ['set-reference-url', 'set-error'],
  setup(props, context) {
    const submitTask = useAsyncTask<SubmissionResultType, []>(async () => {
      return await props.submitter.submit(props.attachment)
    })

    const submit = async () => {
      try {
        const result = await submitTask.perform()
        context.emit('set-reference-url', result.referenceUrl)
      } catch (err) {
        if (axios.isAxiosError(err)) {
          context.emit('set-error', err)
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

    return { confirm, submitTask }
  }
})
</script>
