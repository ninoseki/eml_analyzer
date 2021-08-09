<template>
  <div class="buttons links">
    <LinkComponent
      v-for="link in selectedLinks"
      :link="link"
      :value="value"
      :key="link.name"
    />
  </div>
</template>

<script lang="ts">
import { computed, defineComponent } from "@vue/composition-api";

import LinkComponent from "@/components/links/Link.vue";
import { Links } from "@/links";

export default defineComponent({
  name: "Links",
  props: {
    value: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      required: true,
    },
  },
  components: { LinkComponent },
  setup(props) {
    const selectedLinks = computed(() => {
      if (props.type === undefined) {
        return Links;
      }
      return Links.filter((link) => link.type === props.type);
    });

    return { selectedLinks };
  },
});
</script>
