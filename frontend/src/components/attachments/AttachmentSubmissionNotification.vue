<template>
  <div class="notification is-info is-light">
    <button class="delete" v-if="disposable" @click="dispose"></button>
    The submission result will be available at <a :href="referenceUrl" target="_blank">here</a>.
    Please wait for a while.
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'AttachmentSubmissionInfoMessage',
  props: {
    referenceUrl: {
      type: String,
      required: true
    },
    disposable: {
      type: Boolean,
      default: false
    }
  },
  emits: ['dispose'],
  setup(_, context) {
    const dispose = () => {
      context.emit('dispose')
    }

    return { dispose }
  }
})
</script>
