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
  <div class="grid gap-4">
    <h2 class="text-2xl font-bold middle">Verdicts</h2>
    <Verdict
      class="grid gap-4"
      v-for="verdict in verdicts"
      :key="verdict.name"
      :verdict="verdict"
    />
  </div>
</template>
