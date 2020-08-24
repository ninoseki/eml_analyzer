<template>
  <div class="verdict">
    <b-message
      v-bind:title="title"
      v-bind:type="type"
      v-bind:closable="closable"
      has-icon
    >
      <div v-if="hasDetails">
        <DetailComponent
          v-for="detail in verdict.details"
          v-bind:detail="detail"
          v-bind:key="detail.key"
        />
      </div>
      <div v-else>N/A</div>
    </b-message>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import DetailComponent from "@/components/verdicts/Detail.vue";
import { Verdict } from "@/types";

@Component({
  components: {
    DetailComponent,
  },
})
export default class VerdictComponent extends Vue {
  @Prop() private verdict!: Verdict;

  private closable = false;

  get title(): string {
    return `${this.verdict.name} (score: ${this.verdict.score || "N/A"})`;
  }

  get type(): string {
    return this.verdict.malicious ? "is-warning" : "is-success";
  }

  get hasDetails(): boolean {
    return this.verdict.details.length > 0;
  }
}
</script>

<style scoped>
.verdict {
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>
