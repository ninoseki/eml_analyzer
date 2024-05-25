<script setup lang="ts">
import { computedAsync } from '@vueuse/core'
import { codeToHtml } from 'shiki'

const props = defineProps({
  content: {
    type: String,
    required: true
  },
  contentType: {
    type: String
  }
})

const html = computedAsync(async () => {
  if (props.contentType === 'text/html') {
    return await codeToHtml(props.content, { lang: 'html', theme: 'github-dark-default' })
  }
  return await codeToHtml(props.content, { lang: 'text', theme: 'github-dark-default' })
})
</script>

<template>
  <div v-html="html"></div>
</template>
