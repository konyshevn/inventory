<template>
  <div id="app">
    <CatlgDeviceList></CatlgDeviceList>
    <DocIncomeList></DocIncomeList>

  </div>
</template>

<script>
import DocIncomeList from './components/DocIncomeList.vue'
import DocIncomeItem from './components/DocIncomeItem.vue'
import CatlgDeviceList from './components/CatlgDeviceList.vue'

export default {
  name: 'app',
  components: {
    DocIncomeList,
    DocIncomeItem,
    CatlgDeviceList
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
