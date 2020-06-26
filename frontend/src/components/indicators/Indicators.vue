<template>
  <div>
    <div v-if="hasValues">
      <div class="indicator" v-for="value in values" v-bind:key="value">
        <p>{{ value }}</p>
        <Links v-bind:type="type" v-bind:value="value" />
      </div>
    </div>
    <div v-else>
      N/A
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import Links from "@/components/links/Links.vue";

@Component({
  components: { Links },
})
export default class Indicators extends Vue {
  @Prop() private values!: string[];
  @Prop() private type!: string;

  private hasValues = this.getHasValues();

  getHasValues(): boolean {
    return this.values.length > 0;
  }
}
</script>

<style scoped>
.indicator:nth-child(even) {
  margin-top: 5px;
  margin-bottom: 5px;
  border-top: 1px solid lightgray;
}
</style>
