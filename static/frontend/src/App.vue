<template>
  <div id="app">
    <b-navbar type="light" variant="light" class="header" fixed="top">
      <b-navbar-nav>
        <b-nav-item :to="{name: 'home'}">Главная</b-nav-item>

        <b-nav-item-dropdown text="Документы" right>
          <b-dropdown-item :to="{name: 'doc.list', params: {docType: 'docincome'}}">Оприходование</b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item-dropdown text="Справочники" right>
          <b-dropdown-item :to="{name: 'catlg.list', params: {catlgType: 'device'}}">Устройства</b-dropdown-item>
          <b-dropdown-item :to="{name: 'catlg.list', params: {catlgType: 'deviceType'}}">Типы устройств</b-dropdown-item>
          <b-dropdown-item :to="{name: 'catlg.list', params: {catlgType: 'nomenclature'}}">Номенклатура</b-dropdown-item>
          <b-dropdown-divider></b-dropdown-divider>
          <b-dropdown-item :to="{name: 'catlg.list', params: {catlgType: 'department'}}">Подразделения</b-dropdown-item>
          <b-dropdown-item :to="{name: 'catlg.list', params: {catlgType: 'stock'}}">Склады</b-dropdown-item>
          <b-dropdown-divider></b-dropdown-divider>
          <b-dropdown-item :to="{name: 'catlg.list', params: {catlgType: 'person'}}">Сотрудники</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-navbar>
    <br>
    <router-view></router-view>
    <status-msg></status-msg>
  </div>
</template>

<script>
import StatusMsg from '@/components/common/StatusMsg.vue';
export default {
  name: 'app',
  components: {
    StatusMsg,
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
  margin-top: 40px;
  background: white;
}
.svg-inline--fa {
  color: grey;
}

.row-selected {
background-color: #f2f2f2;
color: #000000;
font-weight: bold;
}

body {
  line-height:1;
}

</style>
