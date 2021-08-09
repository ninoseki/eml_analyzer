<template>
  <pre>
    <code :class="codeType">{{ content }}</code>
  </pre>
</template>

<script lang="ts">
import hljs from "highlight.js/lib/core";
import javascript from "highlight.js/lib/languages/javascript";
import xml from "highlight.js/lib/languages/xml";

// register highlight languages
hljs.registerLanguage("javascript", javascript);
hljs.registerLanguage("xml", xml);

import { computed, defineComponent, onMounted } from "@vue/composition-api";

export default defineComponent({
  name: "Content",
  props: {
    content: {
      type: String,
      required: true,
    },
    contentType: {
      type: String,
    },
  },
  setup(props, context) {
    const codeType = computed(() => {
      if (props.contentType?.includes("html")) {
        return "html";
      }
      return "plaintext hljs";
    });

    const highlightCodeBlocks = () => {
      if (context.root.$el.textContent === "") {
        // do nothing when $el is empty
        return;
      }

      context.root.$el.querySelectorAll("pre code").forEach((block) => {
        if (block.className === "html") {
          hljs.highlightBlock(block as HTMLElement);
        }
        const parent = block.parentElement;
        if (parent !== null) {
          parent.style.backgroundColor = "#282b2e";
        }
      });
    };

    onMounted(() => {
      highlightCodeBlocks();
    });

    return { codeType };
  },
});
</script>
