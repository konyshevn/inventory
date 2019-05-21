<template>
  <div id="app">
    <b-navbar type="light" variant="light" class="header" fixed="top">
      <b-navbar-nav>
        <b-nav-item :to="{name: 'home'}">Главная</b-nav-item>

        <b-nav-item-dropdown text="Документы" right>
          <b-dropdown-item :to="{name: 'docincome.list'}">Оприходование</b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item-dropdown text="Справочники" right>
          <b-dropdown-item :to="{name: 'catlg.device.list'}">Устройства</b-dropdown-item>
          <b-dropdown-item href="#">Settings</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-navbar>
    <br>
    <router-view></router-view>

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
