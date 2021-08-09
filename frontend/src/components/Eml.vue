<template>
  <div>
    <Headers :header="eml.header" />
    <Bodies :bodies="eml.bodies" />
    <Attachments :attachments="eml.attachments" />
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "@vue/composition-api";

import Attachments from "@/components/attachments/Attachments.vue";
import Bodies from "@/components/bodies/Bodies.vue";
import Headers from "@/components/headers/Headers.vue";
import { Eml } from "@/types";
export default defineComponent({
  name: "DnsRecords",
  props: {
    eml: {
      type: Object as PropType<Eml>,
      required: true,
    },
  },
  components: { Attachments, Bodies, Headers },
});
</script>
