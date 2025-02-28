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
  <div class="box">
    <h2 class="is-size-4 has-text-weight-bold middle">Cache</h2>
    <Loading v-if="getCacheKeysTask.isRunning" />
    <ErrorMessage :error="getCacheKeysTask.last?.error" v-if="getCacheKeysTask.isError" />
    <div class="block" v-if="getCacheKeysTask.last?.value && !getCacheKeysTask.last.isRunning">
      <div class="buttons" v-if="getCacheKeysTask.last.value.length > 0">
        <router-link
          class="button is-link is-light"
          :to="{ name: 'Lookup', params: { id: key } }"
          v-for="key in getCacheKeysTask.last.value"
          :key="key"
          >{{ key }}</router-link
        >
      </div>
      <article class="message is-info" v-else>
        <div class="message-body">There is no cache.</div>
      </article>
    </div>
  </div>
</template>
