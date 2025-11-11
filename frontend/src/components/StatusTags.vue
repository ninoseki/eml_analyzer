<script setup lang="ts">
import { useStatus } from '@/composables/useStatus'

const { status } = useStatus()

const toClass = (b: boolean) => {
  return b ? 'badge-success' : 'badge-warning'
}
</script>

<template>
  <div class="flex flex-wrap gap-2">
    <span class="badge" :class="toClass(status.cache || false)">Cache</span>
    <span class="badge" :class="toClass(status.emailRep || false)">EmailRep</span>
    <span class="badge" :class="toClass(status.vt || false)">VirusTotal</span>
    <span class="badge" :class="toClass(status.urlscan || false)">urlscan.io</span>
  </div>
</template>
