<template>
  <div class="navbar-item">
    <div class="dropdown is-active">
      <div class="dropdown-trigger">
        <button class="button" aria-haspopup="true" aria-controls="dropdown-menu">
          <span>Submit to</span>
          <span class="icon is-small">
            <font-awesome-icon icon="angle-down"></font-awesome-icon>
          </span>
        </button>
      </div>
      <div class="dropdown-menu" id="dropdown-menu" role="menu">
        <div class="dropdown-content">
          <div class="dropdown-item" v-for="submitter in selectedSubmitters" :key="submitter.name">
            <SubmitterComponent :submitter="submitter" :value="value" :key="submitter.name" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, type PropType } from 'vue'

import SubmitterComponent from '@/components/submitters/Submitter.vue'
import { Submitters } from '@/submitters'
import type { Attachment, SubmitType } from '@/types'

export default defineComponent({
  name: 'SubmittersComponent',
  props: {
    value: {
      type: Object as PropType<Attachment>,
      required: true
    },
    type: {
      type: String as PropType<SubmitType>,
      required: true
    }
  },
  components: { SubmitterComponent },
  setup(props) {
    const selectedSubmitters = computed(() => {
      if (props.type === undefined) {
        return Submitters
      }
      return Submitters.filter((submitter) => submitter.type === props.type)
    })

    return { selectedSubmitters }
  }
})
</script>
