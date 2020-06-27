<template>
  <div class="table-container">
    <H3>Security headers</H3>
    <FlattenHeaders v-bind:headers="securityHeaders" />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import FlattenHeaders from "@/components/headers/FlattenHeaders.vue";
import H3 from "@/components/ui/h3.vue";
import { Header, HeaderItem, secuirtyKeys } from "@/types";

@Component({
  components: { FlattenHeaders, H3 },
})
export default class SecurityHeaders extends Vue {
  @Prop() private header!: Header;

  private title = "Security headers";

  get securityHeaders(): HeaderItem[] {
    const header = this.header.header;

    const items = secuirtyKeys.map((key) => {
      if (key in header) {
        return { key: key, values: header[key] };
      }
    });
    return items.filter((x): x is HeaderItem => x !== undefined);
  }
}
</script>
