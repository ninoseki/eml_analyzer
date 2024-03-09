<template>
  <div class="block">
    <h2 class="is-size-4 has-text-weight-bold middle">Bodies</h2>
    <BodyComponent v-for="(body, index) in bodies" :key="body.hash" :body="body" :index="index" />
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

import BodyComponent from '@/components/bodies/Body.vue'
import type { BodyType } from '@/schemas'

export default defineComponent({
  name: 'BodiesComponent',
  props: {
    bodies: {
      type: Array as PropType<BodyType[]>,
      required: true
    }
  },
  components: { BodyComponent },
  setup() {}
})
</script>
