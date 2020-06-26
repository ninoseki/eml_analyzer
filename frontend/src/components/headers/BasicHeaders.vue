<template>
  <div class="table-container">
    <H3>Basic headers</H3>
    <table class="table is-fullwidth">
      <tbody>
        <tr>
          <th>Message ID</th>
          <td>{{ header.messageId || "N/A" }}</td>
        </tr>
        <tr>
          <th>Subject</th>
          <td>{{ header.subject }}</td>
        </tr>
        <tr>
          <th>Date</th>
          <td><DatetimeWithDiff v-bind:datetime="header.date" /></td>
        </tr>
        <tr>
          <th>From</th>
          <td>{{ header.from }}</td>
        </tr>
        <tr>
          <th>To</th>
          <td>{{ header.to | toCommaSeparatedString }}</td>
        </tr>
        <tr>
          <th>Cc</th>
          <td>{{ header.cc | toCommaSeparatedString }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import DatetimeWithDiff from "@/components/ui/DatetimeWithDiff.vue";
import H3 from "@/components/ui/h3.vue";
import { Header } from "@/types";

@Component({
  components: {
    DatetimeWithDiff,
    H3,
  },
})
export default class BasicHeaders extends Vue {
  @Prop() private header!: Header;
}
</script>
