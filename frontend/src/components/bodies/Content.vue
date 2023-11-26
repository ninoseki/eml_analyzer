<template>
  <pre>
    <code :class="codeType" ref="code">{{ content }}</code>
  </pre>
</template>

<script lang="ts">
import hljs from "highlight.js/lib/core"
import javascript from "highlight.js/lib/languages/javascript"
import xml from "highlight.js/lib/languages/xml"

// register highlight languages
hljs.registerLanguage("javascript", javascript)
hljs.registerLanguage("xml", xml)

import { computed, defineComponent, onMounted, ref } from "vue"

export default defineComponent({
  name: "ContentComponent",
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
    const code = ref<HTMLElement>()

    const codeType = computed(() => {
      if (props.contentType?.includes("html")) {
        return "html"
      }
      return "plaintext hljs"
    })

    const highlightCodeBlocks = () => {
      if (code.value) {
        if (code.value.textContent === "") {
          return
        }
        if (code.value.className === "html") {
          hljs.highlightBlock(code.value)
        }
        const parent = code.value.parentElement
        if (parent !== null) {
          parent.style.backgroundColor = "#282b2e"
        }
      }
    }

    onMounted(() => {
      highlightCodeBlocks()
    })

    return { codeType, code }
  }
})
</script>
