<template>
  <div>
    <p>{{ utcDatetime }}</p>
  </div>
</template>

<script lang="ts">
import moment from "moment/moment";
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class UTC extends Vue {
  @Prop() private datetime!: string | undefined;

  get utcDatetime(): string {
    if (this.datetime === undefined) {
      return "N/A";
    }
    return moment.utc(this.datetime).format();
  }
}
</script>
