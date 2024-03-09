<template>
  <div class="box">
    <div class="block">
      <h2 class="is-size-4 has-text-weight-bold middle">ID</h2>
      <article class="message is-info">
        <div class="message-body">
          <router-link :to="{ name: 'Lookup', params: { id: response.id } }">{{
            response.id
          }}</router-link>
        </div>
      </article>
    </div>
    <Verdicts :verdicts="response.verdicts" v-if="response.verdicts.length > 0" />
    <Eml :eml="response.eml" />
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

import Eml from '@/components/Eml.vue'
import Verdicts from '@/components/verdicts/Verdicts.vue'
import type { ResponseType } from '@/schemas'

export default defineComponent({
  name: 'ResponseComponent',
  props: {
    response: {
      type: Object as PropType<ResponseType>,
      required: true
    }
  },
  components: { Eml, Verdicts }
})
</script>
