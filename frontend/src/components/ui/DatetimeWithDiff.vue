<template>
  <div>
    <p>{{ datetimeInlocalFormat() }}</p>
  </div>
</template>

<script lang="ts">
import moment from "moment/moment";
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class DatetimeWithDiff extends Vue {
  @Prop() private datetime!: string | undefined;

  datetimeInlocalFormat(): string {
    if (this.datetime === undefined) {
      return "N/A";
    }
    return moment.parseZone(this.datetime).local().format();
  }
}
</script>
