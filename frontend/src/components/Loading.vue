<template>
  <div class="loading-overlay is-active is-full-page">
    <div class="loading-background"></div>
    <div class="loading-icon"></div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'LoadingItem'
})
</script>

<style scoped>
.loading-overlay {
  bottom: 0;
  left: 0;
  position: absolute;
  right: 0;
  top: 0;
  align-items: center;
  display: none;
  justify-content: center;
  overflow: hidden;
  z-index: 29;
}

.loading-overlay.is-active {
  display: flex;
}

.loading-overlay.is-full-page {
  position: fixed;
  z-index: 999;
}

.loading-overlay.is-full-page .loading-icon:after {
  top: calc(50% - 2.5em);
  left: calc(50% - 2.5em);
  width: 5em;
  height: 5em;
}

.loading-overlay .loading-background {
  bottom: 0;
  left: 0;
  position: absolute;
  right: 0;
  top: 0;
  background: #7f7f7f;
  background: rgba(255, 255, 255, 0.5);
}

.loading-overlay .loading-icon {
  position: relative;
}

.loading-overlay .loading-icon:after {
  animation: spinAround 0.5s infinite linear;
  border: 2px solid hsl(0, 0%, 86%);
  border-radius: 9999px;
  border-right-color: transparent;
  border-top-color: transparent;
  content: '';
  display: block;
  height: 1em;
  position: relative;
  width: 1em;
  position: absolute;
  top: calc(50% - 1.5em);
  left: calc(50% - 1.5em);
  width: 3em;
  height: 3em;
  border-width: 0.25em;
}
</style>
