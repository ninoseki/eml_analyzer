<template>
  <div class="table-container">
    <H3Component>Basic headers</H3Component>
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
import { computed, defineComponent, PropType } from "vue"

import Indicators from "@/components/indicators/Indicators.vue"
import H3Component from "@/components/ui/h3.vue"
import UTC from "@/components/ui/UTC.vue"
import { Header } from "@/types"
import { toCommaSeparatedString } from "@/utils/commaSeparated"

export default defineComponent({
  name: "BasicHeaders",
  props: {
    header: {
      type: Object as PropType<Header>,
      required: true
    }
  },
  components: { Indicators, UTC, H3Component },
  setup(props) {
    const emailType = "email"
    const emails = computed(() => {
      return [props.header.from]
    })

    return { emails, emailType, toCommaSeparatedString }
  }
})
</script>
