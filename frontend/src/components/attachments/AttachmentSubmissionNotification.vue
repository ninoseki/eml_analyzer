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
  <div class="notification is-info is-light">
    <button class="delete" v-if="disposable" @click="dispose"></button>
    The submission result will be available at <a :href="referenceUrl" target="_blank">here</a>.
    Please wait for a while.
  </div>
</template>
