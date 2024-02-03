<template>
  <div class="notification is-danger is-light">
    <button class="delete" v-if="disposable" @click="dispose"></button>
    <div v-if="data?.detail">
      <div v-if="typeof data.detail === 'string'">
        {{ data.detail }}
      </div>
      <VueJsonPretty :data="data.detail" v-else></VueJsonPretty>
    </div>
    <p v-else>{{ error }}</p>
  </div>
</template>

<script lang="ts">
import 'vue-json-pretty/lib/styles.css'

import { AxiosError } from 'axios'
import { computed, defineComponent } from 'vue'
import VueJsonPretty from 'vue-json-pretty'

import type { ErrorData } from '@/types'

export default defineComponent({
  name: 'ErrorItem',
  props: {
    error: {
      type: AxiosError,
      required: true
    },
    disposable: {
      type: Boolean,
      default: false
    }
  },
  components: {
    VueJsonPretty
  },
  emits: ['dispose'],
  setup(props, context) {
    const data = computed<ErrorData | undefined>(() => {
      if (props.error.response) {
        return props.error.response?.data as ErrorData
      }
      return undefined
    })

    const dispose = () => {
      context.emit('dispose')
    }

    return { dispose, data }
  }
})
</script>
