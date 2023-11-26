<template>
  <div>
    <p>{{ utcDatetime }}</p>
  </div>
</template>

<script lang="ts">
import dayjs from "dayjs"
import utc from "dayjs/plugin/utc"
import { computed, defineComponent } from "vue"

dayjs.extend(utc)

export default defineComponent({
  name: "UTC",
  props: {
    datetime: {
      type: String
    }
  },
  setup(props) {
    const utcDatetime = computed(() => {
      if (props.datetime === undefined) {
        return "N/A"
      }
      return dayjs.utc(props.datetime).format()
    })

    return { utcDatetime }
  }
})
</script>
