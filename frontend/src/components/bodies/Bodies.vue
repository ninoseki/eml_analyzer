<template>
  <div class="box">
    <H2>Bodies</H2>
    <div v-if="hasBodies">
      <BodyComponent
        v-for="(body, index) in bodies"
        v-bind:key="body.hash"
        v-bind:body="body"
        v-bind:index="index"
      />
    </div>
    <div v-else>
      <p>N/A</p>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import BodyComponent from "@/components/bodies/Body.vue";
import H2 from "@/components/ui/h2.vue";
import { Body } from "@/types";

@Component({
  components: {
    BodyComponent,
    H2,
  },
})
export default class Bodies extends Vue {
  @Prop() private bodies!: Body[];

  private hasBodies = this.getHasBodies();

  getHasBodies(): boolean {
    return this.bodies.length > 0;
  }
}
</script>
