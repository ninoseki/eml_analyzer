<template>
  <div>
    <nav class="navbar">
      <div class="navbar-brand">
        <h3 class="is-size-5 has-text-weight-bold">
          {{ header }}
        </h3>
      </div>
      <div class="navbar-menu">
        <div class="navbar-end">
          <Submitters v-bind:type="sha256Type" v-bind:value="attachment" />
        </div>
      </div>
    </nav>
    <div class="table-container">
      <table class="table is-fullwidth">
        <tbody>
          <tr>
            <th>Filename</th>
            <td>{{ attachment.filename }}</td>
          </tr>
          <tr>
            <th>Size</th>
            <td>{{ filesize }}</td>
          </tr>
          <tr>
            <th>MIME type</th>
            <td>{{ attachment.mimeType || "N/A" }}</td>
          </tr>
          <tr>
            <th>Hash</th>
            <td>
              <Indicators v-bind:type="sha256Type" v-bind:values="values" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import fileSize from "filesize.js";
import { Component, Prop, Vue } from "vue-property-decorator";

import Indicators from "@/components/indicators/Indicators.vue";
import Submitters from "@/components/submitters/Submitters.vue";
import H3 from "@/components/ui/h3.vue";
import { Attachment } from "@/types";

@Component({
  components: { Indicators, H3, Submitters },
})
export default class AttachmentComponent extends Vue {
  @Prop() private attachment!: Attachment;
  @Prop() private index!: number;

  private header = `#${this.index + 1}`;
  private values = [this.attachment.hash.sha256];
  private sha256Type = "sha256";

  get filesize(): string {
    return fileSize(this.attachment.size);
  }
}
</script>
