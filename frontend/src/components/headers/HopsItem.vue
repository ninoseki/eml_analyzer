<template>
  <div class="block" v-if="receivedWithIndexes.length > 0">
    <h3 class="is-size-5 has-text-weight-bold">Hops</h3>
    <div class="table-container">
      <table class="table is-fullwidth is-completely-borderless">
        <thead>
          <tr>
            <th>Hop</th>
            <th>From</th>
            <th>By</th>
            <th>With</th>
            <th>Date (UTC)</th>
            <th>Delay</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="index in receivedWithIndexes" :key="index.index">
            <td>{{ index.index }}</td>
            <td>{{ toCSV(index.received.from || []) }}</td>
            <td>{{ toCSV(index.received.by || []) }}</td>
            <td>{{ index.received.with }}</td>
            <td>
              {{ toUTC(index.received.date) }}
            </td>
            <td>
              <div v-if="index.received.delay">
                {{ humanizeSeconds(index.received.delay) }}
              </div>
              <div v-else>N/A</div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, type PropType } from 'vue'

import type { HeaderType, ReceivedType } from '@/schemas'
import { humanizeSeconds, toCSV, toUTC } from '@/utils'

interface ReceivedWithIndex {
  index: number
  received: ReceivedType
}

const props = defineProps({
  header: {
    type: Object as PropType<HeaderType>,
    required: true
  }
})
const receivedWithIndexes = computed(() => {
  const received = props.header.received || []

  const receivedWithIndex: ReceivedWithIndex[] = received.map((received_, index) => {
    return { index: index + 1, received: received_ }
  })
  return receivedWithIndex
})
</script>
