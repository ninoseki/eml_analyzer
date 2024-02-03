<template>
  <div class="block">
    <h2 class="is-size-4 has-text-weight-bold middle">Verdicts</h2>
    <VerdictComponent v-for="verdict in verdicts" :key="verdict.name" :verdict="verdict" />
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

import VerdictComponent from '@/components/verdicts/Verdict.vue'
import type { Verdict } from '@/types'

export default defineComponent({
  name: 'VerdictsComponent',
  props: {
    verdicts: {
      type: Array as PropType<Verdict[]>,
      required: true
    }
  },
  components: { VerdictComponent },
  setup() {}
})
</script>
