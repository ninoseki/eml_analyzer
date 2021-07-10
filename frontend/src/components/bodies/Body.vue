<template>
  <div class="table-container">
    <H3>{{ header }}</H3>
    <table class="table is-narrow is-fullwidth">
      <tbody>
        <tr>
          <th>Content-Type</th>
          <td>{{ body.contentType || "N/A" }}</td>
        </tr>
        <tr>
          <th>Content</th>
          <td>
            <Content
              v-bind:content="body.content"
              v-bind:contentType="body.contentType"
            />
          </td>
        </tr>
        <tr>
          <th>Extracted URLs</th>
          <td>
            <Indicators v-bind:type="urlType" v-bind:values="body.urls" />
          </td>
        </tr>
        <tr>
          <th>Extracted emails</th>
          <td>
            <Indicators v-bind:type="emailType" v-bind:values="body.emails" />
          </td>
        </tr>
        <tr>
          <th>Extracted domains</th>
          <td>
            <Indicators v-bind:type="domainType" v-bind:values="body.domains" />
          </td>
        </tr>
        <tr>
          <th>Extracted IPv4s</th>
          <td>
            <Indicators
              v-bind:type="ipAddressType"
              v-bind:values="body.ipAddresses"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import Content from "@/components/bodies/Content.vue";
import Indicators from "@/components/indicators/Indicators.vue";
import H3 from "@/components/ui/h3.vue";
import { Body } from "@/types";

@Component({
  components: { Content, Indicators, H3 },
})
export default class BodyComponent extends Vue {
  @Prop() private body!: Body;
  @Prop() private index!: number;

  private domainType = "domain";
  private emailType = "email";
  private ipAddressType = "ip_address";
  private sha256Type = "sha256";
  private urlType = "url";

  private header = `#${this.index + 1}`;
}
</script>
