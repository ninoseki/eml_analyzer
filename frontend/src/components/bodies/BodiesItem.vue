<script setup lang="ts">
import { type PropType } from 'vue'

import BodyComponent from '@/components/bodies/BodyItem.vue'
import type { BodyType } from '@/schemas'

defineProps({
  bodies: {
    type: Array as PropType<BodyType[]>,
    required: true
  }
})
</script>

<template>
  <div class="block">
    <h2 class="is-size-4 has-text-weight-bold middle">Bodies</h2>
    <BodyComponent v-for="(body, index) in bodies" :key="body.hash" :body="body" :index="index" />
  </div>
</template>
