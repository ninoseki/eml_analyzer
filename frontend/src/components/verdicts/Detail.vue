<template>
  <li>
    {{ detail.description }} (score: {{ detail.score || "N/A" }})
    <a
      class="reference"
      target="_blank"
      :href="detail.referenceLink"
      v-if="hasReferenceLink"
    >
      <b-icon pack="fas" icon="link" size="is-small"> </b-icon>
    </a>
  </li>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from "@vue/composition-api";

import { Detail } from "@/types";

export default defineComponent({
  name: "Detail",
  props: {
    detail: {
      type: Object as PropType<Detail>,
      required: true,
    },
  },
  setup(props) {
    const hasReferenceLink = computed(() => {
      return props.detail.referenceLink !== null;
    });
    return { hasReferenceLink };
  },
});
</script>

<style scoped>
.reference {
  margin-left: 5px;
}
</style>
