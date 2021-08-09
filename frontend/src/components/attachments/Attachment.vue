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
            <td>{{ fileSize(attachment.size) }}</td>
          </tr>
          <tr>
            <th>MIME type</th>
            <td>{{ attachment.mimeType || "N/A" }}</td>
          </tr>
          <tr>
            <th>Hash</th>
            <td>
              <Indicators :type="sha256Type" v-bind:values="values" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from "@vue/composition-api";
import fileSize from "filesize.js";

import Indicators from "@/components/indicators/Indicators.vue";
import Submitters from "@/components/submitters/Submitters.vue";
import H3 from "@/components/ui/h3.vue";
import { Attachment } from "@/types";

export default defineComponent({
  name: "Attachement",
  props: {
    attachment: {
      type: Object as PropType<Attachment>,
      required: true,
    },
    index: {
      type: Number,
      required: true,
    },
  },
  components: { H3, Submitters, Indicators },
  setup(props) {
    const header = computed(() => {
      return `#${props.index + 1}`;
    });
    const values = computed(() => {
      return [props.attachment.hash.sha256];
    });
    const sha256Type = "sha256";

    return { header, values, sha256Type, fileSize };
  },
});
</script>
