<script setup lang="ts">
import { type PropType } from 'vue'

import IndicatorButton from '@/components/IndicatorButton.vue'
import type { HeaderType } from '@/schemas'
import { toUTC } from '@/utils'

defineProps({
  header: {
    type: Object as PropType<HeaderType>,
    required: true
  }
})
</script>

<template>
  <h3 class="text-lg font-bold">Basic headers</h3>
  <table class="table w-full break-all">
    <tbody>
      <tr>
        <th class="w-80">Message ID</th>
        <td>{{ header.messageId || 'N/A' }}</td>
      </tr>
      <tr>
        <th class="w-80">Subject</th>
        <td>{{ header.subject }}</td>
      </tr>
      <tr>
        <th class="w-80">Date (UTC)</th>
        <td>
          {{ toUTC(header.date) }}
        </td>
      </tr>
      <tr v-if="header.from">
        <th class="w-80">From</th>
        <td>
          <IndicatorButton :value="header.from" />
        </td>
      </tr>
      <tr v-if="header.to.length > 0">
        <th class="w-80">To</th>
        <td>
          <IndicatorButton :value="email" v-for="email in header.to" :key="email" />
        </td>
      </tr>
      <tr v-if="(header.cc || []).length > 0">
        <th class="w-80">Cc</th>
        <td>
          <IndicatorButton :value="email" v-for="email in header.cc" :key="email" />
        </td>
      </tr>
    </tbody>
  </table>
</template>
