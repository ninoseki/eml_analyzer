<template>
  <li>
    {{ detail.description }} (score: {{ detail.score || "N/A" }})
    <a
      class="reference"
      target="_blank"
      :href="detail.referenceLink"
      v-if="hasReferenceLink"
    >
      <b-icon pack="fas" icon="link" size="is-small"> </b-icon>
    </a>
  </li>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import { Detail } from "@/types";

@Component
export default class DetailCmponent extends Vue {
  @Prop() private detail!: Detail;

  get hasReferenceLink(): boolean {
    return this.detail.referenceLink !== null;
  }
}
</script>

<style scoped>
.reference {
  margin-left: 5px;
}
</style>
