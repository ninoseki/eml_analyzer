<template>
  <div class="box">
    <H2>Headers</H2>
    <BasicHeaders v-bind:header="header" />
    <Hops v-bind:header="header" />
    <SecurityHeaders v-bind:header="header" />
    <XHeaders v-bind:header="header" />
    <OtherHeaders v-bind:header="header" />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import BasicHeaders from "@/components/headers/BasicHeaders.vue";
import Hops from "@/components/headers/Hops.vue";
import OtherHeaders from "@/components/headers/OtherHeaders.vue";
import SecurityHeaders from "@/components/headers/SecurityHeaders.vue";
import XHeaders from "@/components/headers/XHeaders.vue";
import H2 from "@/components/ui/h2.vue";
import { Header } from "@/types";

@Component({
  components: {
    BasicHeaders,
    Hops,
    H2,
    OtherHeaders,
    SecurityHeaders,
    XHeaders,
  },
})
export default class Headers extends Vue {
  @Prop() private header!: Header;
}
</script>
