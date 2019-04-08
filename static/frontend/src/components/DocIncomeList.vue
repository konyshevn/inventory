<template>
  <div class="doc-income-list container">
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Дата</th>
          <th>Номер</th>
          <th>Проведен</th>
          <th>Подразделение</th>
          <th>Склад</th>
          <th>Комментарий</th>
        </tr>
      </thead>
      <tbody>
      <tr v-for="doc in docs" :key="doc.id" v-on:dblclick="clickRow(doc.id)">
        <td>{{doc.doc_date | formatDate}}</td>
        <td>{{doc.doc_num}}</td>
        <td>
          <span v-if="doc.active">Да</span>
          <span v-else></span>
       </td>
        <td>{{getCatlgLabel(doc.department, 'department')}}</td>
        <td>{{getCatlgItemName(doc.stock, 'stock')}}</td>
        <td>{{doc.comment}}</td>
        <a href="123"></a>
      </tr>
    </tbody>
    </table>

  </div>
</template>


<script>
/* eslint-disable no-console */
import Vue from 'vue'
import {HTTP} from '../http-common'
import CatlgCommon from './CatlgCommon.vue'
import moment from 'moment'
var _ = require('lodash');


Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('MM.DD.YYYY hh:mm:ss')
  }
})


export default {
  name: 'DocIncomeList',
  props: {
    //msg: String
  },
  mixins: [CatlgCommon],
  data () {
    return {
      catlgs: {
        'department': [],
        'stock': [],
        'device': []
      },
      docs: []
    }
  },
  methods: {
    fetchDocs: function () {
      var vm = this;
      HTTP.get('docincome/')
        .then(function (response) {
          // установить данные в vm
          var DocsReady = response.data.map(function (doc) {
            return doc
          })
          vm.docs = DocsReady;

        });
    },

    fetchCatlg: function(catlgType){
      var vm = this;
      HTTP.get(catlgType + '/')
        .then(function (response) {
          vm.catlgs[catlgType] = response.data;
        }) 
    },

    getCatlgItemName: function (id, catlgType) {
      var vm = this;
      if (id === null) {
        return "";
      }
      var catlgItem = _.find(vm.catlgs[catlgType], function(item){ return item['id'] == id });
      return catlgItem['name']
    },

    clickRow: function (id) {
      console.log(id);
    }
     
  },
  mounted: function () {
    this.fetchDocs();
    this.fetchCatlg('department');
    this.fetchCatlg('stock');
    //this.fetchCatlg('device');

  },
}


</script>

<style scoped>
tbody tr:hover {
background-color: #f2f2f2;
color: #000000
}
</style>