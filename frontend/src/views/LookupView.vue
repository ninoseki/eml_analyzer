<script setup lang="ts">
import Lookup from '@/components/LookupItem.vue'

defineProps({
  id: {
    type: String,
    required: true
  }
})
</script>

<template>
  <Lookup :id="id" />
</template>
