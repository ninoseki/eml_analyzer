<template>
  <div class="table-container">
    <H3>X headers</H3>
    <FlattenHeaders :headers="xHeaders" />
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from "@vue/composition-api";

import FlattenHeaders from "@/components/headers/FlattenHeaders.vue";
import H3 from "@/components/ui/h3.vue";
import { Header, HeaderItem } from "@/types";

export default defineComponent({
  name: "XHeaders",
  props: {
    header: {
      type: Object as PropType<Header>,
      required: true,
    },
  },
  components: { FlattenHeaders, H3 },
  setup(props) {
    const xHeaders = computed(() => {
      const header = props.header.header;
      const keys = Object.keys(header);
      const xKeys = keys.filter((key) => key.startsWith("x-"));

      const items = xKeys.map((key) => {
        if (key in header) {
          return { key: key, values: header[key] };
        }
      });

      return items.filter((x): x is HeaderItem => x !== undefined);
    });

    return { xHeaders };
  },
});
</script>
