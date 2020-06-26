<template>
  <div>
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

  private title = this.getTitle();
  private type = this.getType();
  private hasDetails = this.getHasDetails();
  private closable = false;

  getTitle(): string {
    return `${this.verdict.name} (score: ${this.verdict.score || "N/A"})`;
  }

  getType(): string {
    return this.verdict.malicious ? "is-warning" : "is-success";
  }

  getHasDetails(): boolean {
    return this.verdict.details.length > 0;
  }
}
</script>
