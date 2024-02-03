<template>
  <Lookup :id="id"></Lookup>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

import Lookup from '@/components/Lookup.vue'

export default defineComponent({
  name: 'LookupView',
  components: { Lookup },
  props: {
    id: {
      type: String,
      required: true
    }
  },
  setup() {}
})
</script>
