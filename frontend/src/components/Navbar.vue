<template>
  <nav role="navigation" aria-label="main navigation" class="navbar is-fixed-top">
    <div class="navbar-brand">
      <a class="navbar-item"><h1 class="title">EML Analyzer</h1></a>
    </div>
    <div class="navbar-menu">
      <div class="navbar-start"></div>
      <div class="navbar-end">
        <router-link class="navbar-item" :to="{ name: 'Home' }">Home</router-link>
        <router-link class="navbar-item" :to="{ name: 'Cache' }">Cache</router-link>
        <a class="navbar-item"><a href="/docs" target="_blank" class="navbar-item">API</a></a>
        <a class="navbar-item"
          ><a href="https://github.com/ninoseki/eml_analyzer" target="_blank" class="navbar-item"
            >GitHub</a
          ></a
        >
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'NavbarComponent'
})
</script>

<style scoped>
.navbar {
  border-bottom: 1px solid lightgray;
}
</style>
