<script setup lang="ts">
import { computed, type PropType } from 'vue'

import Detail from '@/components/verdicts/DetailItem.vue'
import type { DetailType, VerdictType } from '@/schemas'

const props = defineProps({
  verdict: {
    type: Object as PropType<VerdictType>,
    required: true
  }
})

const title = computed(() => {
  return `${props.verdict.name}`
})

const score = computed(() => {
  return props.verdict.score ? props.verdict.score.toFixed(2) : 'N/A'
})

const cardType = computed(() => {
  return props.verdict.malicious ? 'border-warning' : 'border-success'
})

const details = computed((): DetailType[] => {
  if (props.verdict.details.length > 0) {
    return props.verdict.details
  }
  return [{ key: 'N/A', description: 'No details available', score: null }]
})
</script>

<template>
  <div class="card border-1" :class="cardType">
    <div class="card-body">
      <h3 class="card-title text-base">
        {{ title }}
        <div class="badge">{{ score }}</div>
      </h3>
      <ul class="list">
        <Detail v-for="detail in details" :detail="detail" :key="detail.key" />
      </ul>
    </div>
  </div>
</template>
