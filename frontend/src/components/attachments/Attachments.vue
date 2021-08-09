<template>
  <div class="box">
    <H2>Attachments</H2>
    <div v-if="hasAttachments">
      <AttachmentComponent
        v-for="(attachment, index) in attachments"
        :key="attachment.hash.md5"
        :attachment="attachment"
        :index="index"
      />
    </div>
    <div v-else>
      <p>N/A</p>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from "@vue/composition-api";

import AttachmentComponent from "@/components/attachments/Attachment.vue";
import H2 from "@/components/ui/h2.vue";
import { Attachment } from "@/types";

export default defineComponent({
  name: "Attachements",
  props: {
    attachments: {
      type: Array as PropType<Attachment[]>,
      required: true,
    },
  },
  components: { AttachmentComponent, H2 },
  setup(props) {
    const hasAttachments = computed((): boolean => {
      return props.attachments.length > 0;
    });
    return { hasAttachments };
  },
});
</script>
