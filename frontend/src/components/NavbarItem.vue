<script setup lang="ts">
import { useDark, useToggle } from '@vueuse/core'

import StatusTags from '@/components/StatusTags.vue'

const isDark = useDark({
  selector: 'html',
  attribute: 'data-theme',
  valueDark: 'dark',
  valueLight: 'light'
})

const toggleDark = useToggle(isDark)
</script>

<template>
  <nav class="navbar shadow-md">
    <div class="navbar-start">
      <a class="btn btn-ghost text-xl"><h1 class="text-2xl font-bold">EML Analyzer</h1></a>
      <div class="hidden lg:flex">
        <ul class="menu menu-horizontal px-1">
          <li><router-link :to="{ name: 'Home' }" class="btn btn-ghost">Home</router-link></li>
          <li><router-link :to="{ name: 'Cache' }" class="btn btn-ghost">Cache</router-link></li>
          <li><a href="/docs" target="_blank" class="btn btn-ghost">API</a></li>
          <li>
            <a href="https://github.com/ninoseki/eml_analyzer" target="_blank" class="btn btn-ghost"
              >GitHub</a
            >
          </li>
        </ul>
      </div>
    </div>
    <div class="navbar-end">
      <StatusTags />
      <input
        type="checkbox"
        :checked="isDark"
        class="toggle theme-controller ml-2"
        @change="toggleDark()"
      />
    </div>
  </nav>
</template>
