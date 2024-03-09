<template>
  <div class="block">
    <h3 class="is-size-5 has-text-weight-bold">{{ header }}</h3>
    <table class="table is-fullwidth is-completely-borderless">
      <tbody>
        <tr>
          <th>Content-Type</th>
          <td>{{ body.contentType || 'N/A' }}</td>
        </tr>
        <tr>
          <th>Content</th>
          <td>
            <ContentComponent
              :content="body.content"
              :contentType="body.contentType || undefined"
            />
          </td>
        </tr>
        <tr v-if="body.urls.length > 0">
          <th>Extracted URLs</th>
          <td>
            <div class="dropdowns">
              <IndicatorButton :value="url" v-for="url in body.urls" :key="url" />
            </div>
          </td>
        </tr>
        <tr v-if="body.emails.length > 0">
          <th>Extracted emails</th>
          <td>
            <div class="dropdowns">
              <IndicatorButton :value="email" v-for="email in body.emails" :key="email" />
            </div>
          </td>
        </tr>
        <tr v-if="body.domains.length > 0">
          <th>Extracted domains</th>
          <td>
            <div class="dropdowns">
              <IndicatorButton :value="domain" v-for="domain in body.domains" :key="domain" />
            </div>
          </td>
        </tr>
        <tr v-if="body.ipAddresses.length > 0">
          <th>Extracted IPv4s</th>
          <td>
            <div class="dropdowns">
              <IndicatorButton :value="ip" v-for="ip in body.ipAddresses" :key="ip" />
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import truncate from 'just-truncate'
import { computed, defineComponent, type PropType } from 'vue'

import ContentComponent from '@/components/bodies/Content.vue'
import IndicatorButton from '@/components/IndicatorButton.vue'
import type { BodyType } from '@/schemas'

export default defineComponent({
  name: 'BodyComponent',
  props: {
    body: {
      type: Object as PropType<BodyType>,
      required: true
    },
    index: {
      type: Number,
      required: true
    }
  },
  components: { ContentComponent, IndicatorButton },
  setup(props) {
    const header = computed(() => {
      return `#${props.index + 1}`
    })

    return { header, truncate }
  }
})
</script>
