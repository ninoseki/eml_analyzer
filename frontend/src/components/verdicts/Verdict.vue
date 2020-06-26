<template>
  <div class="verdict">
    <b-message
      v-bind:title="title"
      v-bind:type="type"
      v-bind:closable="closable"
    >
      <div v-if="hasDetails">
        <li v-for="detail in verdict.details" v-bind:key="detail.description">
          {{ detail.description }} (score: {{ detail.score || "N/A" }})
        </li>
      </div>
      <div v-else>N/A</div>
    </b-message>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import { Verdict } from "@/types";

@Component
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
