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
          <td><UTC :datetime="header.date" /></td>
        </tr>
        <tr>
          <th>From</th>
          <td>
            <Indicators :type="emailType" :values="emails" />
          </td>
        </tr>
        <tr>
          <th>To</th>
          <td>{{ toCommaSeparatedString(header.to) }}</td>
        </tr>
        <tr>
          <th>Cc</th>
          <td>{{ toCommaSeparatedString(header.cc) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "@vue/composition-api";

import Indicators from "@/components/indicators/Indicators.vue";
import H3 from "@/components/ui/h3.vue";
import UTC from "@/components/ui/UTC.vue";
import { Header } from "@/types";
import { toCommaSeparatedString } from "@/utils/commaSeparated";

export default defineComponent({
  name: "BasicHeaders",
  props: {
    header: {
      type: Object as PropType<Header>,
      required: true,
    },
  },
  components: { Indicators, UTC, H3 },
  setup(props) {
    const emailType = "email";
    const emails = [props.header.from];

    return { emails, emailType, toCommaSeparatedString };
  },
});
</script>
