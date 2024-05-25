<script setup lang="ts">
import { onMounted } from 'vue'

import Navbar from '@/components/Navbar.vue'
import { useStatusStore } from '@/store'

const store = useStatusStore()

onMounted(async () => {
  await store.getStatus()
})
</script>

<template>
  <Navbar />
  <section class="section is-medium">
    <div class="container">
      <router-view />
    </div>
  </section>
</template>

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
</style>
