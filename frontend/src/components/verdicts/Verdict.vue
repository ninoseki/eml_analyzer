<template>
  <div class="verdict">
    <b-message :title="title" :type="type" :closable="closable" has-icon>
      <div v-if="hasDetails">
        <Detail
          v-for="detail in verdict.details"
          :detail="detail"
          :key="detail.key"
        />
      </div>
      <div v-else>N/A</div>
    </b-message>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from "@vue/composition-api";

import Detail from "@/components/verdicts/Detail.vue";
import { Verdict } from "@/types";
export default defineComponent({
  name: "Verdict",
  props: {
    verdict: {
      type: Object as PropType<Verdict>,
      required: true,
    },
  },
  components: { Detail },
  setup(props) {
    const closable = false;
    const title = computed(() => {
      return `${props.verdict.name} (score: ${props.verdict.score || "N/A"})`;
    });
    const type = computed(() => {
      return props.verdict.malicious ? "is-warning" : "is-success";
    });
    const hasDetails = computed(() => {
      return props.verdict.details.length > 0;
    });

    return { closable, type, title, hasDetails };
  },
});
</script>

<style scoped>
.verdict {
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>
