<template>
  <div @click="confirm">
    <span class="icon">
      <img :src="submitter.favicon" alt="favicon" />
    </span>
    <span>{{ submitter.name }}</span>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import { useAsyncTask } from 'vue-concurrency'

import type { Attachment, SubmissionResult, Submitter } from '@/types'

export default defineComponent({
  name: 'SubmitterComponent',
  props: {
    value: {
      type: Object as PropType<Attachment>,
      required: true
    },
    submitter: {
      type: Object as PropType<Submitter>,
      required: true
    }
  },
  setup(props) {
    const confirm = () => {
      const confirmed = window.confirm(
        `Are you sure to submit this attachment to ${props.submitter.name}?`
      )

      if (confirmed) {
        submit()
      }
    }

    const submitTask = useAsyncTask<SubmissionResult, [Attachment]>(async (_, attachment) => {
      return await props.submitter.submit(attachment)
    })

    const submit = async () => {
      submitTask.perform(props.value)
    }

    return { confirm, submitTask }
  }
})
</script>

<style scoped>
img {
  margin-right: 5px;
}
</style>
