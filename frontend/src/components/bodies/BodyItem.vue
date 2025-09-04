<script setup lang="ts">
import { type PropType } from 'vue'

import ContentComponent from '@/components/bodies/ContentItem.vue'
import IndicatorButton from '@/components/IndicatorButton.vue'
import type { BodyType } from '@/schemas'

defineProps({
  body: {
    type: Object as PropType<BodyType>,
    required: true
  },
  inlineAttachments: {
    type: Object,
    required: true
  },
})
</script>

<template>
  <ContentComponent :content="body.content" :inlineAttachments="inlineAttachments" :contentType="body.contentType || undefined" />
  <table class="table w-full break-all">
    <tbody>
      <tr>
        <th class="w-80">Content-Type</th>
        <td>{{ body.contentType || 'N/A' }}</td>
      </tr>
      <tr v-if="body.urls.length > 0">
        <th class="w-80">Extracted URLs</th>
        <td>
          <div class="dropdowns">
            <IndicatorButton :value="url" v-for="url in body.urls" :key="url" />
          </div>
        </td>
      </tr>
      <tr v-if="body.emails.length > 0">
        <th class="w-80">Extracted emails</th>
        <td>
          <div class="dropdowns">
            <IndicatorButton :value="email" v-for="email in body.emails" :key="email" />
          </div>
        </td>
      </tr>
      <tr v-if="body.domains.length > 0">
        <th class="w-80">Extracted domains</th>
        <td>
          <div class="dropdowns">
            <IndicatorButton :value="domain" v-for="domain in body.domains" :key="domain" />
          </div>
        </td>
      </tr>
      <tr v-if="body.ipAddresses.length > 0">
        <th class="w-80">Extracted IPv4s</th>
        <td>
          <div class="dropdowns">
            <IndicatorButton :value="ip" v-for="ip in body.ipAddresses" :key="ip" />
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</template>
