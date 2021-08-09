<template>
  <div class="box">
    <H2>Bodies</H2>
    <div v-if="hasBodies">
      <BodyComponent
        v-for="(body, index) in bodies"
        :key="body.hash"
        :body="body"
        :index="index"
      />
    </div>
    <div v-else>
      <p>N/A</p>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from "@vue/composition-api";

import BodyComponent from "@/components/bodies/Body.vue";
import H2 from "@/components/ui/h2.vue";
import { Body } from "@/types";
export default defineComponent({
  name: "Bodies",
  props: {
    bodies: {
      type: Array as PropType<Body[]>,
      required: true,
    },
  },
  components: { BodyComponent, H2 },
  setup(props) {
    const hasBodies = computed((): boolean => {
      return props.bodies.length > 0;
    });
    return { hasBodies };
  },
});
</script>
