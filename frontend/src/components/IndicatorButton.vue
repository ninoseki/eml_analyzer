<script setup lang="ts">
import { useClipboard } from '@vueuse/core'
import truncate from 'just-truncate'
import { computed } from 'vue'

import { Links } from '@/links'
import type { IndicatorType } from '@/schemas'
import { getIndicatorType } from '@/utils'

const props = defineProps({
  value: {
    type: String,
    required: true
  }
})

const indicatorType = computed<IndicatorType | undefined>(() => {
  return getIndicatorType(props.value)
})

const links = computed(() => {
  return Links.filter((link) => link.type === indicatorType.value)
})

const copyToClipboard = () => {
  const { copy } = useClipboard()
  copy(props.value)
}
</script>

<template>
  <div class="dropdown dropdown-end dropdown-hover">
    <div tabindex="0" role="button" class="btn">
      <span>{{ truncate(value, 64) }}</span>
      <font-awesome-icon icon="angle-down" aria-hidden="true" class="w-4 h-4"></font-awesome-icon>
    </div>
    <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-[1] w-52 p-2 shadow">
      <li>
        <a @click="copyToClipboard">
          <font-awesome-icon icon="copy" class="w-4 h-4"></font-awesome-icon>
          <span>Copy to clipboard</span>
        </a>
      </li>
      <li v-for="(link, index) in links" :key="index">
        <a :href="link.href(value)" target="_blank">
          <img :src="link.favicon" alt="favicon" class="w-4 h-4" />
          <span>{{ link.name }}</span>
        </a>
      </li>
    </ul>
  </div>
</template>
