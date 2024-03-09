<template>
  <div class="tags">
    <span class="tag is-light" :class="toClass(status.cache || false)">Cache</span>
    <span class="tag is-light" :class="toClass(status.emailRep || false)">EmailRep</span>
    <span class="tag is-light" :class="toClass(status.vt || false)">VirusTotal</span>
    <span class="tag is-light" :class="toClass(status.inquest || false)">InQuest</span>
    <span class="tag is-light" :class="toClass(status.urlscan || false)">urlscan.io</span>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

import type { Status } from '@/types'

export default defineComponent({
  name: 'StatusTags',
  props: {
    status: {
      type: Object as PropType<Status>,
      required: true
    }
  },
  setup() {
    const toClass = (b: boolean) => {
      return b ? 'is-success' : 'is-warning'
    }

    return { toClass }
  }
})
</script>
