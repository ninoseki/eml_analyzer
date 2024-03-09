<template>
  <div class="block">
    <h3 class="is-size-5 has-text-weight-bold">Basic headers</h3>
    <table class="table is-fullwidth is-completely-borderless">
      <tbody>
        <tr>
          <th>Message ID</th>
          <td>{{ header.messageId || 'N/A' }}</td>
        </tr>
        <tr>
          <th>Subject</th>
          <td>{{ header.subject }}</td>
        </tr>
        <tr>
          <th>Date (UTC)</th>
          <td>
            {{ toUTC(header.date) }}
          </td>
        </tr>
        <tr v-if="header.from">
          <th>From</th>
          <td>
            <div class="dropdowns">
              <IndicatorButton :value="header.from" />
            </div>
          </td>
        </tr>
        <tr v-if="header.to.length > 0">
          <th>To</th>
          <td>
            <div class="dropdowns">
              <IndicatorButton :value="email" v-for="email in header.to" :key="email" />
            </div>
          </td>
        </tr>
        <tr v-if="(header.cc || []).length > 0">
          <th>Cc</th>
          <td>
            <div class="dropdowns">
              <IndicatorButton :value="email" v-for="email in header.cc" :key="email" />
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

import IndicatorButton from '@/components/IndicatorButton.vue'
import type { HeaderType } from '@/schemas'
import { toUTC } from '@/utils'

export default defineComponent({
  name: 'BasicHeaders',
  props: {
    header: {
      type: Object as PropType<HeaderType>,
      required: true
    }
  },
  components: { IndicatorButton },
  setup() {
    return { toUTC }
  }
})
</script>
