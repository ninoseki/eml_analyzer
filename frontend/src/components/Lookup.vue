<template>
  <Loading v-if="lookupTask.isRunning" />
  <ErrorMessage :error="lookupTask.last?.error" v-if="lookupTask.isError" />
  <Response :response="lookupTask.last.value" v-if="lookupTask.last?.value" />
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue'
import { useAsyncTask } from 'vue-concurrency'

import { API } from '@/api'
import ErrorMessage from '@/components/ErrorMessage.vue'
import Loading from '@/components/Loading.vue'
import Response from '@/components/Response.vue'
import type { ResponseType } from '@/schemas'

export default defineComponent({
  name: 'LookupItem',
  props: {
    id: {
      type: String,
      required: true
    }
  },
  components: {
    Response,
    Loading,
    ErrorMessage
  },
  setup(props) {
    const lookupTask = useAsyncTask<ResponseType, []>(async () => {
      return await API.lookup(props.id)
    })

    onMounted(async () => {
      await lookupTask.perform()
    })

    return { lookupTask }
  }
})
</script>
