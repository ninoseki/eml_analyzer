<template>
  <div class="table-container">
    <H3>X headers</H3>
    <FlattenHeaders v-bind:headers="xHeaders" />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import FlattenHeaders from "@/components/headers/FlattenHeaders.vue";
import H3 from "@/components/ui/h3.vue";
import { Header, HeaderItem } from "@/types";

@Component({
  components: { FlattenHeaders, H3 },
})
export default class XHeaders extends Vue {
  @Prop() private header!: Header;

  private xHeaders: HeaderItem[] = this.getXHeaders();

  getXHeaders(): HeaderItem[] {
    const header = this.header.header;
    const keys = Object.keys(header);
    const xKeys = keys.filter((key) => key.startsWith("x-"));

    const items = xKeys.map((key) => {
      if (key in header) {
        return { key: key, values: header[key] };
      }
    });

    return items.filter((x): x is HeaderItem => x !== undefined);
  }
}
</script>
