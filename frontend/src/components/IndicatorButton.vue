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
  <div class="dropdown is-hoverable is-right">
    <div class="dropdown-trigger">
      <button class="button is-light is-link">
        <span>{{ truncate(value, 64) }}</span>
        <span class="icon is-small">
          <font-awesome-icon icon="angle-down" aria-hidden="true"></font-awesome-icon>
        </span>
      </button>
    </div>
    <div class="dropdown-menu">
      <div class="dropdown-content">
        <a class="dropdown-item" @click="copyToClipboard">
          <span class="icon">
            <font-awesome-icon icon="copy"></font-awesome-icon>
          </span>
          <span>Copy to clipboard</span>
        </a>
        <a
          :href="link.href(value)"
          class="dropdown-item"
          target="_blank"
          v-for="(link, index) in links"
          :key="index"
        >
          <span class="icon">
            <img :src="link.favicon" alt="favicon" />
          </span>
          <span>{{ link.name }}</span>
        </a>
      </div>
    </div>
  </div>
</template>
