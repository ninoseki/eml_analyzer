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
  <div class="grid gap-4">
    <div class="grid gap-4" v-if="status.cache">
      <h2 class="text-2xl font-bold middle">Cache</h2>
      <div class="card border-1 border-info">
        <div class="card-body">
          <h3 class="card-title text-base">ID</h3>
          <router-link :to="{ name: 'Lookup', params: { id: response.id } }">{{
            response.id
          }}</router-link>
        </div>
      </div>
    </div>
    <Verdicts :verdicts="response.verdicts" v-if="response.verdicts.length > 0" />
    <Eml :eml="response.eml" />
  </div>
</template>
