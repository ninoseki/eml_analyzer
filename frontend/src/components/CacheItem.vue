<script setup lang="ts">
import { onMounted } from 'vue'
import { useAsyncTask } from 'vue-concurrency'

import { API } from '@/api'
import ErrorMessage from '@/components/ErrorMessage.vue'
import Loading from '@/components/LoadingItem.vue'

const getCacheKeysTask = useAsyncTask<string[], []>(async () => {
  return await API.getCacheKeys()
})

onMounted(async () => {
  await getCacheKeysTask.perform()
})
</script>

<template>
  <div class="grid gap-4">
    <h2 class="text-2xl font-bold middle">Cache</h2>
    <Loading v-if="getCacheKeysTask.isRunning" />
    <ErrorMessage :error="getCacheKeysTask.last?.error" v-if="getCacheKeysTask.isError" />
    <div v-if="getCacheKeysTask.last?.value && !getCacheKeysTask.last.isRunning">
      <div class="flex flex-wrap gap-2" v-if="getCacheKeysTask.last.value.length > 0">
        <router-link
          class="btn"
          :to="{ name: 'Lookup', params: { id: key } }"
          v-for="key in getCacheKeysTask.last.value"
          :key="key"
          >{{ key }}</router-link
        >
      </div>
      <div class="alert alert-info" v-else>
        <span>There is no cache.</span>
      </div>
    </div>
  </div>
</template>
