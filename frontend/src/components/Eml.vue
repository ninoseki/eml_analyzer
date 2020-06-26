<template>
  <div>
    <Headers v-bind:header="eml.header" />
    <Bodies v-bind:bodies="eml.bodies" />
    <Attachments v-bind:attachments="eml.attachments" />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import Attachments from "@/components/attachments/Attachments.vue";
import Bodies from "@/components/bodies/Bodies.vue";
import Headers from "@/components/headers/Headers.vue";
import { Eml } from "@/types";

@Component({
  components: {
    Attachments,
    Bodies,
    Headers,
  },
})
export default class EmlComponent extends Vue {
  @Prop() private eml!: Eml;
}
</script>
