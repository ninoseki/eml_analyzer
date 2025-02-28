<script setup lang="ts">
import { type PropType } from 'vue'

import type { StatusType } from '@/schemas'

defineProps({
  status: {
    type: Object as PropType<StatusType>,
    required: true
  }
})

const toClass = (b: boolean) => {
  return b ? 'is-success' : 'is-warning'
}
</script>

<template>
  <div class="tags">
    <span class="tag is-light" :class="toClass(status.cache || false)">Cache</span>
    <span class="tag is-light" :class="toClass(status.emailRep || false)">EmailRep</span>
    <span class="tag is-light" :class="toClass(status.vt || false)">VirusTotal</span>
    <span class="tag is-light" :class="toClass(status.inquest || false)">InQuest</span>
    <span class="tag is-light" :class="toClass(status.urlscan || false)">urlscan.io</span>
  </div>
</template>
