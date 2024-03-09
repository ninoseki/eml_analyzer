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
        <div class="dropdown-item">
          <button class="button is-borderless is-small" @click="copyToClipboard">
            <span class="icon">
              <font-awesome-icon icon="copy"></font-awesome-icon>
            </span>
            <span>Copy to clipboard</span>
          </button>
        </div>
        <div class="dropdown-item" v-for="(link, index) in links" :key="index">
          <a :href="link.href(value)" class="button is-borderless is-small" target="_blank">
            <span class="icon">
              <img :src="link.favicon" alt="favicon" />
            </span>
            <span>{{ link.name }}</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { useClipboard } from '@vueuse/core'
import truncate from 'just-truncate'
import { computed, defineComponent } from 'vue'

import { Links } from '@/links'
import type { IndicatorType } from '@/schemas'
import { getIndicatorType } from '@/utils'

export default defineComponent({
  name: 'IndicatorButton',
  props: {
    value: {
      type: String,
      required: true
    }
  },
  setup(props) {
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

    return { truncate, links, indicatorType, copyToClipboard }
  }
})
</script>
