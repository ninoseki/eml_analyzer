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
  return b ? 'badge-success' : 'badge-warning'
}
</script>

<template>
  <div class="flex flex-wrap gap-2">
    <span class="badge" :class="toClass(status.cache || false)">Cache</span>
    <span class="badge" :class="toClass(status.emailRep || false)">EmailRep</span>
    <span class="badge" :class="toClass(status.vt || false)">VirusTotal</span>
    <span class="badge" :class="toClass(status.inquest || false)">InQuest</span>
    <span class="badge" :class="toClass(status.urlscan || false)">urlscan.io</span>
  </div>
</template>
