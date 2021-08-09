<template>
  <div class="box">
    <H2>Verdicts</H2>
    <div v-if="hasVerdicts">
      <VerdictComponent
        v-for="verdict in verdicts"
        :key="verdict.name"
        :verdict="verdict"
      />
    </div>
    <div v-else>
      <p>N/A</p>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from "@vue/composition-api";

import H2 from "@/components/ui/h2.vue";
import VerdictComponent from "@/components/verdicts/Verdict.vue";
import { Verdict } from "@/types";

export default defineComponent({
  name: "Verdicts",
  props: {
    verdicts: {
      type: Array as PropType<Verdict[]>,
      required: true,
    },
  },
  components: { VerdictComponent, H2 },
  setup(props) {
    const hasVerdicts = computed((): boolean => {
      return props.verdicts.length > 0;
    });
    return { hasVerdicts };
  },
});
</script>
