<template>
  <div class="table-container">
    <H3>Hops</H3>
    <div v-if="hasReceivedWithIndex">
      <b-table :data="receivedWithIndex">
        <template slot-scope="props">
          <b-table-column field="index" label="Hop">
            {{ props.row.index }}
          </b-table-column>
          <b-table-column field="from" label="From">
            {{ props.row.received.from | toCommaSeparatedString }}
          </b-table-column>
          <b-table-column field="by" label="By">
            {{ props.row.received.by | toCommaSeparatedString }}
          </b-table-column>
          <b-table-column field="with" label="With">
            {{ props.row.received.with }}
          </b-table-column>
          <b-table-column field="date" label="Date (UTC)">
            <UTC v-bind:datetime="props.row.received.date" />
          </b-table-column>
          <b-table-column field="delay" label="Delay">
            {{ props.row.received.delay | secondsToHumanize }}
          </b-table-column>
        </template>
      </b-table>
    </div>
    <div v-else>
      N/A
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import H3 from "@/components/ui/h3.vue";
import UTC from "@/components/ui/UTC.vue";
import { Header, Received } from "@/types";

interface ReceivedWithIndex {
  index: number;
  received: Received;
}

@Component({
  components: {
    UTC,
    H3,
  },
})
export default class Hops extends Vue {
  @Prop() private header!: Header;

  get receivedWithIndex(): ReceivedWithIndex[] {
    const received = this.header.received || [];

    const receivedWithIndex: ReceivedWithIndex[] = received.map(
      (recived_, index) => {
        return { index: index + 1, received: recived_ };
      }
    );

    return receivedWithIndex;
  }

  get hasReceivedWithIndex(): boolean {
    return this.receivedWithIndex.length > 0;
  }
}
</script>
