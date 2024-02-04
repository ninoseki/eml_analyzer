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

<script lang="ts">
import linkifyString from 'linkify-string'
import { computed, defineComponent, type PropType } from 'vue'

import type { Detail } from '@/types'

export default defineComponent({
  name: 'DetailComponent',
  props: {
    detail: {
      type: Object as PropType<Detail>,
      required: true
    }
  },
  setup(props) {
    const html = computed(() => {
      return linkifyString(`${props.detail.description} (score: ${props.detail.score || 'N/A'})`, {
        validate: {
          url: (value) => /^https?:\/\//.test(value)
        }
      })
    })

    return { html }
  }
})
</script>
