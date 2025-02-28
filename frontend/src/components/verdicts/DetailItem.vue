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
  return linkifyString(`${props.detail.description} (score: ${props.detail.score || 'N/A'})`, {
    validate: {
      url: (value) => /^https?:\/\//.test(value)
    }
  })
})
</script>

<template>
  <li>
    <span v-html="html"></span>
    <a target="_blank" :href="detail.referenceLink" v-if="detail.referenceLink">
      <span class="icon is-small">
        <font-awesome-icon icon="link"></font-awesome-icon>
      </span>
    </a>
  </li>
</template>
