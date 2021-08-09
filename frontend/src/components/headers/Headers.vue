<template>
  <div class="box">
    <H2>Headers</H2>
    <BasicHeaders :header="header" />
    <Hops :header="header" />
    <SecurityHeaders :header="header" />
    <XHeaders :header="header" />
    <OtherHeaders :header="header" />
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "@vue/composition-api";

import BasicHeaders from "@/components/headers/BasicHeaders.vue";
import Hops from "@/components/headers/Hops.vue";
import OtherHeaders from "@/components/headers/OtherHeaders.vue";
import SecurityHeaders from "@/components/headers/SecurityHeaders.vue";
import XHeaders from "@/components/headers/XHeaders.vue";
import H2 from "@/components/ui/h2.vue";
import { Header } from "@/types";

export default defineComponent({
  name: "Headers",
  props: {
    header: {
      type: Object as PropType<Header>,
      required: true,
    },
  },
  components: {
    BasicHeaders,
    Hops,
    H2,
    OtherHeaders,
    SecurityHeaders,
    XHeaders,
  },
});
</script>
