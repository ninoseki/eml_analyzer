<script setup lang="ts">
import { computed, type PropType } from 'vue'

import Detail from '@/components/verdicts/DetailItem.vue'
import type { VerdictType } from '@/schemas'

const props = defineProps({
  verdict: {
    type: Object as PropType<VerdictType>,
    required: true
  }
})

const title = computed(() => {
  return `${props.verdict.name} (score: ${props.verdict.score || 'N/A'})`
})
const type = computed(() => {
  return props.verdict.malicious ? 'is-warning' : 'is-success'
})
</script>

<template>
  <article class="message mt-2 mb-2" :class="type">
    <div class="message-header">
      <p>{{ title }}</p>
    </div>
    <div class="message-body content">
      <div v-if="verdict.details.length > 0">
        <Detail v-for="detail in verdict.details" :detail="detail" :key="detail.key" />
      </div>
      <div v-else>N/A</div>
    </div>
  </article>
</template>
