<template>
  <div class="doc-income-list">
    <table>
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

      <tr v-for="doc in docs" :key="doc.id">
        <td>{{doc.doc_date | formatDate}}</td>
        <td>{{doc.doc_num}}</td>
        <td>
          <span v-if="doc.active">Проведен</span>
          <span v-else>Не проведен</span>
       </td>
        <td>{{doc.department | getCatlgItemName('department')}}</td>
        <td>{{doc.stock | getCatlgItemName('stock')}}</td>
        <td>{{doc.comment}}</td>
      </tr>
    
    </table>
    <pre> {{$data}} </pre>
  </div>
</template>


<script>
import Vue from 'vue'
import {HTTP} from '../http-common'
import moment from 'moment'

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('MM.DD.YYYY hh:mm:ss')
  }
})

Vue.filter('getCatlgItemName', function(id, catlgType) {
  var catlgItemName = "";
  if (id) {
    const request = HTTP.get(catlgType + '/' + id + '/')
    .then(function (response) {
      catlgItemName = response.data['name'];
      return catlgItemName
    });


    return request
    .then(result => { 
      console.log(result); 
      return result; })
    .catch(error => {
      console.error(error); 
      return Promise.reject(error); 
    });


  }
})

export default {
  name: 'DocIncomeList',
  props: {
    //msg: String
  },
  data () {
    return {
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
            //doc.editing = false;
            return doc
          })
          vm.docs = DocsReady;
        });
    },
  },
  mounted: function () {
    this.fetchDocs()
  },

}
</script>