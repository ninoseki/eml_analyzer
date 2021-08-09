<template>
  <b-navbar :fixed-top="true">
    <template slot="brand">
      <b-navbar-item>
        <h1 class="title">EML analyzer</h1>
      </b-navbar-item>
    </template>
    <template slot="end">
      <b-navbar-item tag="router-link" :to="{ path: '/' }">Home</b-navbar-item>
      <b-navbar-item>
        <a href="/docs" target="_blank" class="navbar-item">API</a>
      </b-navbar-item>
      <b-navbar-item>
        <a
          href="https://github.com/ninoseki/eml_analyzer"
          target="_blank"
          class="navbar-item"
          >GitHub</a
        >
      </b-navbar-item>
    </template>
  </b-navbar>
</template>

<style>
.navbar {
  border-bottom: 1px solid lightgray;
}
</style>
