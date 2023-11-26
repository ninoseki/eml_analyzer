<template>
  <a :href="link.href(value)" class="button" type="button" target="_blank">
    <span class="icon">
      <img :src="link.favicon" alt="favicon" />
    </span>
    <span>{{ link.name }}</span>
  </a>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue"

import { Link } from "@/types"

export default defineComponent({
  name: "LinkComponent",
  props: {
    value: {
      type: String,
      required: true
    },
    link: {
      type: Object as PropType<Link>,
      required: true
    }
  }
})
</script>

<style scoped>
img {
  margin-right: 5px;
}
</style>
