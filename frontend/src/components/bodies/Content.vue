<template>
  <pre v-html="html" v-if="html"></pre>
  <pre v-else>{{ content }}</pre>
</template>

<script lang="ts">
import '@wooorm/starry-night/style/both'

import { createStarryNight } from '@wooorm/starry-night'
import textHtmlBasic from '@wooorm/starry-night/text.html.basic'
import { toHtml } from 'hast-util-to-html'
import { defineComponent, onMounted, ref } from 'vue'

export default defineComponent({
  name: 'ContentComponent',
  props: {
    content: {
      type: String,
      required: true
    },
    contentType: {
      type: String
    }
  },
  setup(props) {
    const html = ref<string>()

    onMounted(async () => {
      if (props.contentType === 'text/html') {
        const starryNight = await createStarryNight([textHtmlBasic])
        const scope = starryNight.flagToScope('html')
        if (scope) {
          const tree = starryNight.highlight(props.content, scope)
          html.value = toHtml(tree)
        }
      }
    })

    return { html }
  }
})
</script>
