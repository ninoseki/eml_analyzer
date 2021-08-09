<template>
  <div>
    <div v-if="hasValues">
      <div class="indicator" v-for="value in values" :key="value">
        <p class="value">{{ value }}</p>
        <Links :type="type" :value="value" />
      </div>
    </div>
    <div v-else>N/A</div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from "@vue/composition-api";

import Links from "@/components/links/Links.vue";

export default defineComponent({
  name: "Indicators",
  props: {
    values: {
      type: Array as PropType<string[]>,
      required: true,
    },
    type: {
      type: String,
      required: true,
    },
  },
  components: { Links },

  setup(props) {
    const hasValues = computed(() => {
      return props.values.length > 0;
    });

    return { hasValues };
  },
});
</script>

<style scoped>
.value {
  margin-top: 5px;
  margin-bottom: 5px;
}

.indicator:not(:first-child) {
  margin-top: 5px;
  margin-bottom: 5px;
  border-top: 1px solid lightgray;
}
</style>
