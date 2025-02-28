<script setup lang="ts">
import { computed, type PropType } from 'vue'

import Eml from '@/components/EmlItem.vue'
import Verdicts from '@/components/verdicts/VerdictsItem.vue'
import type { ResponseType } from '@/schemas'
import { useStatusStore } from '@/store'

defineProps({
  response: {
    type: Object as PropType<ResponseType>,
    required: true
  }
})

const store = useStatusStore()
const status = computed(() => store.$state)
</script>

<template>
  <div class="box">
    <div class="block">
      <h2 class="is-size-4 has-text-weight-bold middle">ID</h2>
      <article class="message is-info">
        <div class="message-body">
          <router-link :to="{ name: 'Lookup', params: { id: response.id } }" v-if="status.cache">{{
            response.id
          }}</router-link>
          <p v-else>{{ response.id }}</p>
        </div>
      </article>
    </div>
    <Verdicts :verdicts="response.verdicts" v-if="response.verdicts.length > 0" />
    <Eml :eml="response.eml" />
  </div>
</template>
