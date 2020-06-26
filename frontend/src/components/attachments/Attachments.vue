<template>
  <div class="box">
    <H2>Attachments</H2>
    <div v-if="hasAttachments">
      <AttachmentComponent
        v-for="(attachment, index) in attachments"
        v-bind:key="attachment.hash.md5"
        v-bind:attachment="attachment"
        v-bind:index="index"
      />
    </div>
    <div v-else>
      <p>N/A</p>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import AttachmentComponent from "@/components/attachments/Attachment.vue";
import H2 from "@/components/ui/h2.vue";
import { Attachment } from "@/types";

@Component({
  components: {
    AttachmentComponent,
    H2,
  },
})
export default class Attachments extends Vue {
  @Prop() private attachments!: Attachment[];

  private hasAttachments = this.getHasAttachments();

  getHasAttachments(): boolean {
    return this.attachments.length > 0;
  }
}
</script>
