<template>
  <div class="doc-income-item container">

    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Устройство</th>
          <th>Сотрудник</th>
          <th>Количество</th>
          <th>Комментарий</th>
        </tr>
      </thead>
      <tbody>
      <tr v-for="rec in doc.table_unit" :key="rec.id">
        <td>{{getCatlgLabel(rec.device, 'device')}}</td>
        <td>{{getCatlgLabel(rec.person, 'person')}}</td>
        <td>{{rec.qty}}</td>
        <td>{{rec.comment}}</td>
      </tr>
      </tbody>
    </table>

  </div>
</template>


<script>
/* eslint-disable no-console */
import Vue from 'vue'
import {HTTP} from '../http-common'
import moment from 'moment'
var _ = require('lodash');


Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('MM.DD.YYYY hh:mm:ss')
  }
})


export default {
  name: 'DocIncomeItem',
  props: {
    //msg: String
  },
  data () {
    return {
      catlgs: {
        'department': [],
        'stock': [],
        'device': [],
        'person': [],
        'nomenclature': [],
        'devicetype': []
      },
      doc: {}
    }
  },
  methods: {
    fetchDoc: function (id) {
      var vm = this;
      HTTP.get('docincome/' + id + '/')
        .then(function (response) {
          vm.doc = response.data;
        })
    },

    fetchCatlg: function(catlgType){
      var vm = this;
      HTTP.get(catlgType + '/')
        .then(function (response) {
          vm.catlgs[catlgType] = response.data;
        }) 
    },

    getCatlgItem: function (id, catlgType) {
      var vm = this;
      if (id === null) {
        return "";
      }
      var catlgItem = _.find(vm.catlgs[catlgType], function(item){ return item['id'] == id });
      return catlgItem
    },

    clickRow: function (id) {
      console.log(id);
    },

    getCatlgLabel: function(id, catlgName){
      var vm = this;
      var label = "unknown";
      var item = vm.getCatlgItem(id, catlgName);
      switch(catlgName){
        case 'device':
          var devicetype = vm.getCatlgItem(item['device_type'], 'devicetype')['name'];
          var nomenclature = vm.getCatlgItem(item['name'], 'nomenclature')['name'];
          label = devicetype + ' ' + nomenclature;
          break;

        case 'person':
          label = item['surname'] + ' ' + item['name'];
          break;

        case 'department':
          label = item['name'];
          break;
      }
      return label;
    },
     
  },
  mounted: function () {
    this.fetchCatlg('department');
    this.fetchCatlg('stock');
    this.fetchCatlg('person');
    this.fetchCatlg('device');
    this.fetchCatlg('devicetype');
    this.fetchCatlg('nomenclature');
    this.fetchDoc(225);
  }
}
   



</script>

<style scoped>
tbody tr:hover {
background-color: #f2f2f2;
color: #000000
}
</style>