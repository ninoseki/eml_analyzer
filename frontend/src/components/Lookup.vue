<template>
  <Loading v-if="lookupTask.isRunning"></Loading>
  <ErrorMessage :error="lookupTask.last?.error" v-if="lookupTask.isError" />
  <ResponseComponent :response="lookupTask.last.value" v-if="lookupTask.last?.value" />
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue'
import { useAsyncTask } from 'vue-concurrency'

import { API } from '@/api'
import ErrorMessage from '@/components/ErrorMessage.vue'
import Loading from '@/components/Loading.vue'
import ResponseComponent from '@/components/Response.vue'
import type { Response } from '@/types'

export default defineComponent({
  name: 'LookupItem',
  props: {
    id: {
      type: String,
      required: true
    }
  },
  components: {
    ResponseComponent,
    Loading,
    ErrorMessage
  },
  setup(props) {
    const lookupTask = useAsyncTask<Response, []>(async () => {
      return await API.lookup(props.id)
    })

    onMounted(async () => {
      await lookupTask.perform()
    })

    return { lookupTask }
  }
})
</script>
