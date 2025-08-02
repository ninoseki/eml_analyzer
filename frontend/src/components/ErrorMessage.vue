<script setup lang="ts">
import 'vue-json-pretty/lib/styles.css'

import { AxiosError } from 'axios'
import { computed } from 'vue'
import VueJsonPretty from 'vue-json-pretty'

import type { ErrorDataType } from '@/schemas'

const props = defineProps({
  error: {
    type: AxiosError,
    required: true
  },
  disposable: {
    type: Boolean,
    default: false
  }
})
const emits = defineEmits(['dispose'])

const data = computed<ErrorDataType | undefined>(() => {
  if (props.error.response) {
    return props.error.response?.data as ErrorDataType
  }
  return undefined
})

const dispose = () => {
  emits('dispose')
}
</script>

<template>
  <div class="alert alert-error">
    <button
      class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
      v-if="disposable"
      @click="dispose"
    >
      ✕
    </button>
    <div v-if="data?.detail">
      <div v-if="typeof data.detail === 'string'">
        {{ data.detail }}
      </div>
      <VueJsonPretty :data="data.detail" v-else />
    </div>
    <p v-else>{{ error }}</p>
  </div>
</template>
