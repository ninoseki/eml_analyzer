<script setup lang="ts">
import linkifyString from 'linkify-string'
import { computed, type PropType } from 'vue'

import type { DetailType } from '@/schemas'

const props = defineProps({
  detail: {
    type: Object as PropType<DetailType>,
    required: true
  }
})

const html = computed(() => {
  return linkifyString(props.detail.description, {
    validate: {
      url: (value) => /^https?:\/\//.test(value)
    }
  })
})
const score = computed(() => {
  return props.detail.score ? props.detail.score.toFixed(2) : 'N/A'
})
</script>

<template>
  <li class="list-row">
    <div v-html="html"></div>
    <div>
      <span class="badge">{{ score }}</span>
    </div>
    <div v-if="detail.referenceLink">
      <a target="_blank" :href="detail.referenceLink" class="btn btn-ghost btn-xs ml-2">
        <font-awesome-icon icon="link" class="w-3 h-3"></font-awesome-icon>
      </a>
    </div>
  </li>
</template>
