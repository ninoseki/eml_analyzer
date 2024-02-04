<template>
  <div class="box">
    <h2 class="is-size-4 has-text-weight-bold middle">Cache</h2>
    <Loading v-if="getCacheKeysTask.isRunning"></Loading>
    <ErrorMessage :error="getCacheKeysTask.last?.error" v-if="getCacheKeysTask.isError" />
    <div class="block" v-if="getCacheKeysTask.last?.value && !getCacheKeysTask.last.isRunning">
      <div class="buttons">
        <router-link
          class="button is-link is-light"
          :to="{ name: 'Lookup', params: { id: key } }"
          v-for="key in getCacheKeysTask.last.value"
          :key="key"
          >{{ key }}</router-link
        >
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue'
import { useAsyncTask } from 'vue-concurrency'

import { API } from '@/api'
import ErrorMessage from '@/components/ErrorMessage.vue'
import Loading from '@/components/Loading.vue'

export default defineComponent({
  name: 'HomeView',
  components: {
    ErrorMessage,
    Loading
  },
  setup() {
    const getCacheKeysTask = useAsyncTask<string[], []>(async () => {
      return await API.getCacheKeys()
    })

    onMounted(async () => {
      await getCacheKeysTask.perform()
    })

    return { getCacheKeysTask }
  }
})
</script>
