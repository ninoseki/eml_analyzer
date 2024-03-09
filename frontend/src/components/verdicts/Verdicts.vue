<template>
  <div class="block">
    <h2 class="is-size-4 has-text-weight-bold middle">Verdicts</h2>
    <Verdict v-for="verdict in verdicts" :key="verdict.name" :verdict="verdict" />
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

import Verdict from '@/components/verdicts/Verdict.vue'
import type { VerdictType } from '@/schemas'

export default defineComponent({
  name: 'VerdictsComponent',
  props: {
    verdicts: {
      type: Array as PropType<VerdictType[]>,
      required: true
    }
  },
  components: { Verdict },
  setup() {}
})
</script>
