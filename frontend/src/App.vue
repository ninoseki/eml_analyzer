<script setup lang="ts">
import Navbar from '@/components/NavbarItem.vue'
</script>

<template>
  <Navbar />
  <section class="py-16">
    <div class="container mx-auto px-4">
      <router-view />
    </div>
  </section>
</template>
