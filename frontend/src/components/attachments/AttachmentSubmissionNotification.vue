<script setup lang="ts">
defineProps({
  referenceUrl: {
    type: String,
    required: true
  },
  disposable: {
    type: Boolean,
    default: false
  }
})

const emits = defineEmits(['dispose'])
const dispose = () => {
  emits('dispose')
}
</script>

<template>
  <div class="alert alert-info">
    <button
      class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
      v-if="disposable"
      @click="dispose"
    >
      ✕
    </button>
    <span
      >The submission result will be available at <a :href="referenceUrl" target="_blank">here</a>.
      Please wait for a while.</span
    >
  </div>
</template>
