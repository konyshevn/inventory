<template>
  <div id="app">
    <DocIncomeList></DocIncomeList>
  </div>
</template>

<script>
import DocIncomeList from './components/DocIncomeList.vue'

export default {
  name: 'app',
  components: {
    DocIncomeList
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
