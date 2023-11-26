<template>
  <b-navbar :fixed-top="true">
    <template v-slot:brand>
      <b-navbar-item>
        <h1 class="title">EML analyzer</h1>
      </b-navbar-item>
    </template>
    <template v-slot:end>
      <b-navbar-item>
        <a href="/" class="navbar-item">Home</a>
      </b-navbar-item>
      <b-navbar-item>
        <a href="/docs" target="_blank" class="navbar-item">API</a>
      </b-navbar-item>
      <b-navbar-item>
        <a href="https://github.com/ninoseki/eml_analyzer" target="_blank" class="navbar-item"
          >GitHub</a
        >
      </b-navbar-item>
    </template>
  </b-navbar>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
  name: "NavbarComponent"
})
</script>

<style scoped>
.navbar {
  border-bottom: 1px solid lightgray;
}
</style>
