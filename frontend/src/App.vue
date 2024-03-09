<template>
  <Navbar></Navbar>
  <section class="section is-medium">
    <div class="container">
      <router-view />
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue'

import Navbar from '@/components/Navbar.vue'
import { useStatusStore } from '@/store'

export default defineComponent({
  name: 'App',
  components: {
    Navbar
  },
  setup() {
    const store = useStatusStore()

    onMounted(async () => {
      store.getStatus()
    })
  }
})
</script>

<style>
html {
  background-color: #fafafa !important;
}

pre {
  white-space: pre;
  white-space: pre-wrap;
  word-break: break-all;
  word-wrap: break-word;
}

table.is-fullwidth th {
  width: 360px;
}

.dropdowns .dropdown {
  margin-bottom: 0.5rem;
}

.dropdowns .dropdown:not(:last-child):not(.is-fullwidth) {
  margin-right: 0.5rem;
}
</style>
