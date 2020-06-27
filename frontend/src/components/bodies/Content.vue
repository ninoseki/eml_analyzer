<template>
  <pre>
    <code v-bind:class="codeType">{{ content }}</code>
  </pre>
</template>

<script lang="ts">
import hljs from "highlight.js/lib/core";
import javascript from "highlight.js/lib/languages/javascript";
import xml from "highlight.js/lib/languages/xml";
import { Component, Prop, Vue } from "vue-property-decorator";

// register highlight languages
hljs.registerLanguage("javascript", javascript);
hljs.registerLanguage("xml", xml);

@Component
export default class Content extends Vue {
  @Prop() private content!: string;
  @Prop() private contentType!: string | undefined;

  get codeType(): string {
    if (this.contentType?.includes("html")) {
      return "html";
    }
    return "plaintext hljs";
  }

  highlightCodeBlocks() {
    if (this.$el.textContent === "") {
      // do nothing when $el is empty
      return;
    }

    this.$el.querySelectorAll("pre code").forEach((block) => {
      if (block.className === "html") {
        hljs.highlightBlock(block as HTMLElement);
      }
      const parent = block.parentElement;
      if (parent !== null) {
        parent.style.backgroundColor = "#282b2e";
      }
    });
  }

  mounted() {
    this.highlightCodeBlocks();
  }
}
</script>
