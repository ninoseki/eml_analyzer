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

<script lang="ts">
import { computed, defineComponent, type PropType } from 'vue'

import Detail from '@/components/verdicts/Detail.vue'
import type { VerdictType } from '@/schemas'

export default defineComponent({
  name: 'VerdictComponent',
  props: {
    verdict: {
      type: Object as PropType<VerdictType>,
      required: true
    }
  },
  components: { Detail },
  setup(props) {
    const closable = false
    const title = computed(() => {
      return `${props.verdict.name} (score: ${props.verdict.score || 'N/A'})`
    })
    const type = computed(() => {
      return props.verdict.malicious ? 'is-warning' : 'is-success'
    })

    return { closable, type, title }
  }
})
</script>
