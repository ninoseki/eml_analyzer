<template>
  <div class="box">
    <H2Component>Bodies</H2Component>
    <div v-if="hasBodies">
      <BodyComponent v-for="(body, index) in bodies" :key="body.hash" :body="body" :index="index" />
    </div>
    <div v-else>
      <p>N/A</p>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from "vue"

import BodyComponent from "@/components/bodies/Body.vue"
import H2Component from "@/components/ui/H2.vue"
import { Body } from "@/types"
export default defineComponent({
  name: "BodiesComponent",
  props: {
    bodies: {
      type: Array as PropType<Body[]>,
      required: true
    }
  },
  components: { BodyComponent, H2Component },
  setup(props) {
    const hasBodies = computed((): boolean => {
      return props.bodies.length > 0
    })
    return { hasBodies }
  }
})
</script>
