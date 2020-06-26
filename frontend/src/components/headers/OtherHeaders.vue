<template>
  <div class="table-container">
    <H3>Other headers</H3>
    <FlattenHeaders v-bind:headers="otherHeaders" />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import FlattenHeaders from "@/components/headers/FlattenHeaders.vue";
import H3 from "@/components/ui/h3.vue";
import { basicKeys, Header, HeaderItem, secuirtyKeys } from "@/types";

@Component({
  components: { FlattenHeaders, H3 },
})
export default class OtherHeaders extends Vue {
  @Prop() private header!: Header;

  private title = "Other headers";

  get otherHeaders(): HeaderItem[] {
    const header = this.header.header;
    const keys = Object.keys(header);
    const otherKeys = keys
      .filter((key) => !key.startsWith("x-"))
      .filter((key) => secuirtyKeys.indexOf(key) == -1)
      .filter((key) => basicKeys.indexOf(key) == -1);

    const items = otherKeys.map((key) => {
      if (key in header) {
        return { key: key, values: header[key] };
      }
    });

    return items.filter((x): x is HeaderItem => x !== undefined);
  }
}
</script>
