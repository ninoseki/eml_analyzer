<template>
  <table class="table is-fullwidth" v-if="hasFlattenHeaders">
    <tbody>
      <tr v-for="header in flattenHeaders" v-bind:key="header.id">
        <th>{{ header.key }}</th>
        <td>{{ header.value }}</td>
      </tr>
    </tbody>
  </table>
  <div v-else>
    <p>N/A</p>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import { HeaderItem } from "@/types";

interface FlattenHeader {
  id: string;
  key: string;
  value: string | number;
}

@Component
export default class FlattenHeaders extends Vue {
  @Prop() private headers!: HeaderItem[];

  get flattenHeaders(): FlattenHeader[] {
    const headers = [];
    let index = 0;
    for (const header of this.headers) {
      const key = header.key;
      const values = header.values;
      for (const value of values) {
        index += 1;
        headers.push({
          id: key + index.toString(),
          key: key,
          value: value,
        });
      }
    }
    return headers;
  }

  get hasFlattenHeaders(): boolean {
    return this.flattenHeaders.length > 0;
  }
}
</script>
