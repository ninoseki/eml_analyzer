<script setup lang="ts">
import { onMounted } from 'vue'
import { useAsyncTask } from 'vue-concurrency'

import { API } from '@/api'
import ErrorMessage from '@/components/ErrorMessage.vue'
import Loading from '@/components/Loading.vue'
import Response from '@/components/ResponseItem.vue'
import type { ResponseType } from '@/schemas'

const props = defineProps({
  id: {
    type: String,
    required: true
  }
})

const lookupTask = useAsyncTask<ResponseType, []>(async () => {
  return await API.lookup(props.id)
})

onMounted(async () => {
  await lookupTask.perform()
})
</script>

<template>
  <Loading v-if="lookupTask.isRunning" />
  <ErrorMessage :error="lookupTask.last?.error" v-if="lookupTask.isError" />
  <Response :response="lookupTask.last.value" v-if="lookupTask.last?.value" />
</template>
