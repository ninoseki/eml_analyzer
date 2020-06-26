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
import { Component, Prop, Vue } from "vue-property-decorator";

import { Hash } from "@/types";

@Component
export default class Hashes extends Vue {
  @Prop() private hash!: Hash;
}
</script>
