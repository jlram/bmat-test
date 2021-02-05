<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png" height="150">
    <Main msg="Works Backend Test"/>
  </div>
</template>

<script>
import Main from './pages/Main.vue'

export default {
  name: 'App',
  components: {
    Main
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
