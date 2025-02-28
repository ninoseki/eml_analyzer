<script setup lang="ts">
import { type PropType } from 'vue'

import Verdict from '@/components/verdicts/VerdictItem.vue'
import type { VerdictType } from '@/schemas'

defineProps({
  verdicts: {
    type: Array as PropType<VerdictType[]>,
    required: true
  }
})
</script>

<template>
  <div class="block">
    <h2 class="is-size-4 has-text-weight-bold middle">Verdicts</h2>
    <Verdict v-for="verdict in verdicts" :key="verdict.name" :verdict="verdict" />
  </div>
</template>
