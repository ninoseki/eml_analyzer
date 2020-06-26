<template>
  <div>
    <Verdicts v-bind:verdicts="response.verdicts" />
    <Eml v-bind:eml="response.eml" />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import Eml from "@/components/Eml.vue";
import Verdicts from "@/components/verdicts/Verdicts.vue";
import { Response } from "@/types";

@Component({
  components: {
    Eml,
    Verdicts,
  },
})
export default class ResponseComponent extends Vue {
  @Prop() private response!: Response;
}
</script>
