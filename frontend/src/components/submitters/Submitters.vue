<template>
  <b-dropdown aria-role="list">
    <button class="button" slot="trigger" slot-scope="{ active }">
      <b-icon pack="fas" icon="upload" size="is-small" />
      <span>Submit to</span>
      <b-icon :icon="active ? 'menu-up' : 'menu-down'"></b-icon>
    </button>

    <b-dropdown-item
      v-for="submitter in selectedSubmitters"
      v-bind:key="submitter.name"
      aria-role="listitem"
    >
      <SubmitterComponent
        v-bind:submitter="submitter"
        v-bind:value="value"
        v-bind:key="submitter.name"
      />
    </b-dropdown-item>
  </b-dropdown>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import SubmitterComponent from "@/components/submitters/Submitter.vue";
import { Submitters } from "@/submitters";
import { Attachment, Submitter, SubmitType } from "@/types";

@Component({
  components: {
    SubmitterComponent,
  },
})
export default class SubmittersComponent extends Vue {
  @Prop() private value!: Attachment;
  @Prop() private type!: SubmitType;

  get selectedSubmitters(): Submitter[] {
    if (this.type === undefined) {
      return Submitters;
    }

    return Submitters.filter((submitter) => submitter.type === this.type);
  }
}
</script>
