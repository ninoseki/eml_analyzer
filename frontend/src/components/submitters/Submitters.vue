<template>
  <div class="navbar-item">
    <b-dropdown aria-role="list">
      <button class="button" slot="trigger" slot-scope="{ active }">
        <b-icon pack="fas" icon="upload" size="is-small" />
        <span>Submit to</span>
        <b-icon :icon="active ? 'menu-up' : 'menu-down'"></b-icon>
      </button>

      <b-dropdown-item
        v-for="submitter in selectedSubmitters"
        :key="submitter.name"
        aria-role="listitem"
      >
        <SubmitterComponent
          :submitter="submitter"
          :value="value"
          :key="submitter.name"
        />
      </b-dropdown-item>
    </b-dropdown>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from "@vue/composition-api";

import SubmitterComponent from "@/components/submitters/Submitter.vue";
import { Submitters } from "@/submitters";
import { Attachment, SubmitType } from "@/types";

export default defineComponent({
  name: "Submitters",
  props: {
    value: {
      type: Object as PropType<Attachment>,
      required: true,
    },
    type: {
      type: Object as PropType<SubmitType>,
      required: true,
    },
  },
  components: { SubmitterComponent },
  setup(props) {
    const selectedSubmitters = computed(() => {
      if (props.type === undefined) {
        return Submitters;
      }
      return Submitters.filter((submitter) => submitter.type === props.type);
    });

    return { selectedSubmitters };
  },
});
</script>
