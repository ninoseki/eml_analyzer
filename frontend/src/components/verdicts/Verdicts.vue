<template>
  <div class="box">
    <H2>Verdicts</H2>
    <div v-if="hasVerdicts">
      <VerdictComponent
        v-for="verdict in verdicts"
        v-bind:key="verdict.name"
        v-bind:verdict="verdict"
      />
    </div>
    <div v-else>
      <p>N/A</p>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import H2 from "@/components/ui/h2.vue";
import VerdictComponent from "@/components/verdicts/Verdict.vue";
import { Verdict } from "@/types";

@Component({
  components: {
    VerdictComponent,
    H2,
  },
})
export default class Verdicts extends Vue {
  @Prop() private verdicts!: Verdict[];

  get hasVerdicts(): boolean {
    return this.verdicts.length > 0;
  }
}
</script>
