<script setup lang="ts">
import { onMounted } from 'vue'

import Navbar from '@/components/NavbarItem.vue'
import { useStatusStore } from '@/store'

const store = useStatusStore()

onMounted(async () => {
  await store.getStatus()
})
</script>

<template>
  <Navbar />
  <section class="py-16">
    <div class="container mx-auto px-4">
      <router-view />
    </div>
  </section>
</template>
