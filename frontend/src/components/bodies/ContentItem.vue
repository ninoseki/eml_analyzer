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
  const render = async () => {
    if (props.contentType === 'text/html') {
      return await codeToHtml(props.content, { lang: 'html', theme: 'github-dark-default' })
    }
    return await codeToHtml(props.content, { lang: 'text', theme: 'github-dark-default' })
  }
  return await render()
})
</script>

<template>
  <div class="mockup-code w-full px-6 my-4 bg-[#0d1117]" v-html="html"></div>
</template>

<style>
pre.shiki > code {
  white-space: pre-wrap;
  word-break: break-all;
  word-wrap: break-word;
}

pre.shiki {
  overflow-x: auto;
}

pre.shiki::before {
  content: none !important;
  display: none !important;
}
</style>
