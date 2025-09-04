<script setup lang="ts">
import { computedAsync } from '@vueuse/core'
import { codeToHtml } from 'shiki'
import { computed } from 'vue'

const props = defineProps({
  content: {
    type: String,
    required: true
  },
  contentType: {
    type: String
  },
  inlineAttachments: {
    type: Object,
    required: true
  },
})

const isHTMLContent = computed(() => {
  return (props.contentType || '').startsWith('text/html')
})

const HTMLContent = computed(() => {
  const CIDPrefix = "cid:";

  const parser = new DOMParser();
  const parsedHTML = parser.parseFromString(props.content, 'text/html');
  const imageTags = parsedHTML.querySelectorAll("img");

  imageTags.forEach(tag => {
    if(tag.src.startsWith(CIDPrefix)){

      const imageCID = tag.src.slice(CIDPrefix.length);
      const inlinedImage = props.inlineAttachments[imageCID];

      if(inlinedImage !== undefined){
        tag.src = inlinedImage;
      }
    }
  });

  return parsedHTML.documentElement.innerHTML;
})

const code = computedAsync(async () => {
  const render = async () => {
    if (isHTMLContent.value) {
      return await codeToHtml(props.content, { lang: 'html', theme: 'github-dark-default' })
    }
    return await codeToHtml(props.content, { lang: 'text', theme: 'github-dark-default' })
  }
  return await render()
})

const gridColumns = computed(() => {
  return isHTMLContent.value ? 'grid-cols-2' : 'grid-cols-1'
})
</script>

<template>
  <div :class="['grid', gridColumns]">
    <div class="mockup-code w-full h-96 overflow-scroll px-6 my-4 bg-[#0d1117]" v-html="code"></div>
    <iframe
      class="w-full h-96 border-0 px-6 my-4"
      :srcdoc="HTMLContent"
      sandbox=""
      v-if="isHTMLContent"
    ></iframe>
  </div>
</template>

<style>
pre.shiki > code {
  white-space: pre-wrap;
  word-break: break-all;
  word-wrap: break-word;
}

pre.shiki::before {
  content: none !important;
  display: none !important;
}
</style>
