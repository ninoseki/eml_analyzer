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
          <th>Date (UTC)</th>
          <td><UTC v-bind:datetime="header.date" /></td>
        </tr>
        <tr>
          <th>From</th>
          <td>
            <Indicators v-bind:type="emailType" v-bind:values="emails" />
          </td>
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

import Indicators from "@/components/indicators/Indicators.vue";
import H3 from "@/components/ui/h3.vue";
import UTC from "@/components/ui/UTC.vue";
import { Header } from "@/types";

@Component({
  components: {
    Indicators,
    UTC,
    H3,
  },
})
export default class BasicHeaders extends Vue {
  @Prop() private header!: Header;

  private emailType = "email";
  private emails = [this.header.from];
}
</script>
