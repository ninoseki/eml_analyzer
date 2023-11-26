<template>
  <div class="table-container">
    <H3Component>Hops</H3Component>
    <div v-if="hasReceivedWithIndex">
      <b-table :data="receivedWithIndex">
        <b-table-column field="index" label="Hop" v-slot="props">
          {{ props.row.index }}
        </b-table-column>
        <b-table-column field="from" label="From" v-slot="props">
          {{ toCommaSeparatedString(props.row.received.from) }}
        </b-table-column>
        <b-table-column field="by" label="By" v-slot="props">
          {{ toCommaSeparatedString(props.row.received.by) }}
        </b-table-column>
        <b-table-column field="with" label="With" v-slot="props">
          {{ props.row.received.with }}
        </b-table-column>
        <b-table-column field="date" label="Date (UTC)" v-slot="props">
          <UTC :datetime="props.row.received.date" />
        </b-table-column>
        <b-table-column field="delay" label="Delay" v-slot="props">
          {{ secondsToHumanize(props.row.received.delay) }}
        </b-table-column>
      </b-table>
    </div>
    <div v-else>N/A</div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from "vue"

import H3Component from "@/components/ui/H3.vue"
import { Header, Received } from "@/types"
import { toCommaSeparatedString } from "@/utils/commaSeparated"
import { secondsToHumanize } from "@/utils/secondsToHumanize"

interface ReceivedWithIndex {
  index: number
  received: Received
}

export default defineComponent({
  name: "HopsComponent",
  props: {
    header: {
      type: Object as PropType<Header>,
      required: true
    }
  },
  components: { H3Component },
  setup(props) {
    const receivedWithIndex = computed(() => {
      const received = props.header.received || []

      const receivedWithIndex: ReceivedWithIndex[] = received.map((recived_, index) => {
        return { index: index + 1, received: recived_ }
      })
      return receivedWithIndex
    })

    const hasReceivedWithIndex = computed(() => {
      return receivedWithIndex.value.length > 0
    })

    return {
      hasReceivedWithIndex,
      receivedWithIndex,
      toCommaSeparatedString,
      secondsToHumanize
    }
  }
})
</script>
