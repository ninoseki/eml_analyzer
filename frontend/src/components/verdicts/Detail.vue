<template>
  <li>
    {{ detail.description }} (score: {{ detail.score || 'N/A' }})
    <a target="_blank" :href="detail.referenceLink" v-if="detail.referenceLink">
      <span class="icon is-small">
        <font-awesome-icon icon="link"></font-awesome-icon>
      </span>
    </a>
  </li>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

import type { Detail } from '@/types'

export default defineComponent({
  name: 'DetailComponent',
  props: {
    detail: {
      type: Object as PropType<Detail>,
      required: true
    }
  },
  setup() {}
})
</script>
