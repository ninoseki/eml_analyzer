<template>
  <a
    v-bind:href="link.href(value)"
    class="button"
    type="button"
    target="_blank"
  >
    <span class="icon">
      <img v-bind:src="link.favicon" alt="favicon" />
    </span>
    <span>{{ link.name }}</span>
  </a>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import { Link } from "@/types";

@Component
export default class LinkComponent extends Vue {
  @Prop() private value!: string;
  @Prop() private link!: Link;
}
</script>

<style scoped>
img {
  margin-right: 5px;
}
</style>
