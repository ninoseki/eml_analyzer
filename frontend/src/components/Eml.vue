<template>
  <Headers :header="eml.header" />
  <Bodies :bodies="eml.bodies" v-if="eml.bodies.length > 0" />
  <Attachments :attachments="eml.attachments" v-if="eml.attachments.length > 0" />
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

import Attachments from '@/components/attachments/Attachments.vue'
import Bodies from '@/components/bodies/Bodies.vue'
import Headers from '@/components/headers/Headers.vue'
import type { Eml } from '@/types'

export default defineComponent({
  name: 'EmlComponent',
  props: {
    eml: {
      type: Object as PropType<Eml>,
      required: true
    }
  },
  components: { Attachments, Bodies, Headers }
})
</script>
