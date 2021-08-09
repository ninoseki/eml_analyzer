<template>
  <h3 class="is-size-5 has-text-weight-bold">
    <slot />
  </h3>
</template>

<script lang="ts">
import { defineComponent } from "@vue/composition-api";

export default defineComponent({
  name: "H3",
});
</script>

<style scoped>
h3 {
  padding-bottom: 5px;
  margin-bottom: 5px;
  border-bottom: 1px solid lightgray;
}
</style>
