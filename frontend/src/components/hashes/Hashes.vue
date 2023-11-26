<template>
  <div class="table-container">
    <table class="table is-fullwidth">
      <tbody>
        <tr>
          <th>MD5</th>
          <td>{{ hash.md5 }}</td>
        </tr>
        <tr>
          <th>SHA1</th>
          <td>{{ hash.sha1 }}</td>
        </tr>
        <tr>
          <th>SHA256</th>
          <td>{{ hash.sha256 }}</td>
        </tr>
        <tr>
          <th>SHA512</th>
          <td>{{ hash.sha512 }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue"

import { Hash } from "@/types"
export default defineComponent({
  name: "HashesComponent",
  props: {
    hash: {
      type: Object as PropType<Hash>,
      required: true
    }
  }
})
</script>
