<template>
  <Upload></Upload>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

import Upload from '@/components/Upload.vue'

export default defineComponent({
  name: 'HomeView',
  components: { Upload },
  setup() {}
})
</script>
