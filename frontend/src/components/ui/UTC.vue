<template>
  <div>
    <p>{{ utcDatetime }}</p>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent } from "@vue/composition-api";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";

dayjs.extend(utc);

export default defineComponent({
  name: "UTC",
  props: {
    datetime: {
      type: String,
    },
  },
  setup(props) {
    const utcDatetime = computed(() => {
      if (props.datetime === undefined) {
        return "N/A";
      }
      return dayjs.utc(props.datetime).format();
    });

    return { utcDatetime };
  },
});
</script>

function comptued(arg0: () => string) { throw new Error("Function not
implemented."); }
