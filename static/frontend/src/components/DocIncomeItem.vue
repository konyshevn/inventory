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
        <td>{{getCatlgItemName(rec.device, 'device')}}</td>
        <td>{{getCatlgItemName(rec.person, 'person')}}</td>
        <td>{{rec.qty}}</td>
        <td>{{rec.comment}}</td>
      </tr>
      </tbody>
    </table>
    <pre> {{$data}} </pre>
  </div>
</template>


<script>

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
        'person': []
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
    },

    resolveLabel: function(item, mapFields){
      var vm = this;
      for (var itemField in mapFields){
        var model = mapFields[itemField][0]
        var modelField = mapFields[itemField][1]
        console.log(model)
        console.log(modelField)
      }
    }
     
  },
  mounted: function () {
    this.fetchDoc(245);
    this.fetchCatlg('department');
    this.fetchCatlg('stock');
    this.fetchCatlg('person');
    this.fetchCatlg('device');
    this.resolveLabel({'name': 652, 'device_type': 128}, {'name':['nomenclature', 'name'], 'device_type': ['device_type', 'name']})
  }
    
}


</script>

<style scoped>
tbody tr:hover {
background-color: #f2f2f2;
color: #000000
}
</style>