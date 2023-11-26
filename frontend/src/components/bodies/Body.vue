<template>
  <div class="table-container">
    <H3Component>{{ header }}</H3Component>
    <table class="table is-narrow is-fullwidth">
      <tbody>
        <tr>
          <th>ContentComponent-Type</th>
          <td>{{ body.ContentComponentType || "N/A" }}</td>
        </tr>
        <tr>
          <th>ContentComponent</th>
          <td>
            <ContentComponent
              :ContentComponent="body.ContentComponent"
              :ContentComponentType="body.ContentComponentType"
            />
          </td>
        </tr>
        <tr>
          <th>Extracted URLs</th>
          <td>
            <Indicators :type="urlType" :values="body.urls" />
          </td>
        </tr>
        <tr>
          <th>Extracted emails</th>
          <td>
            <Indicators :type="emailType" :values="body.emails" />
          </td>
        </tr>
        <tr>
          <th>Extracted domains</th>
          <td>
            <Indicators :type="domainType" :values="body.domains" />
          </td>
        </tr>
        <tr>
          <th>Extracted IPv4s</th>
          <td>
            <Indicators :type="ipAddressType" :values="body.ipAddresses" />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from "vue"

import ContentComponent from "@/components/bodies/Content.vue"
import Indicators from "@/components/indicators/Indicators.vue"
import H3Component from "@/components/ui/h3.vue"
import { Body } from "@/types"
export default defineComponent({
  name: "BodyComponent",
  props: {
    body: {
      type: Object as PropType<Body>,
      required: true
    },
    index: {
      type: Number,
      required: true
    }
  },
  components: { H3Component, ContentComponent, Indicators },
  setup(props) {
    const domainType = "domain"
    const emailType = "email"
    const ipAddressType = "ip_address"
    const sha256Type = "sha256"
    const urlType = "url"

    const header = computed(() => {
      return `#${props.index + 1}`
    })

    return {
      header,
      domainType,
      emailType,
      ipAddressType,
      sha256Type,
      urlType
    }
  }
})
</script>
