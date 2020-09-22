<template>
  <div>
    <p>{{ utcDatetime }}</p>
  </div>
</template>

<script lang="ts">
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import { Component, Prop, Vue } from "vue-property-decorator";

dayjs.extend(utc);

@Component
export default class UTC extends Vue {
  @Prop() private datetime!: string | undefined;

  get utcDatetime(): string {
    if (this.datetime === undefined) {
      return "N/A";
    }
    return dayjs.utc(this.datetime).format();
  }
}
</script>
