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
      <tr v-for="doc in docs['docincome']" :key="doc.id" v-on:dblclick="clickRow(doc.id)">
        <td>{{doc.doc_date | formatDate}}</td>
        <td>{{doc.doc_num}}</td>
        <td>
          <span v-if="doc.active">Да</span>
          <span v-else></span>
        </td>
        <td>{{getCatlgLabel('department', doc.department)}}</td>
        <td>{{getCatlgLabel('stock', doc.stock)}}</td>
        <td>{{doc.comment}}</td>
      </tr>
    </tbody>
    </table>

  </div>
</template>


<script>
/* eslint-disable no-console */
import Vue from 'vue';
import {HTTP} from '../http-common';
import moment from 'moment';
var _ = require('lodash');
import CatlgCommon from './CatlgCommon.vue';
import DocCommon from './DocCommon.vue';

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
  mixins: [CatlgCommon, DocCommon],
  data () {
    return {
    }
  },
  methods: {

    clickRow: function (id) {
      console.log(id);
    }
     
  },
  mounted: function () {
    this.fetchDocs('docincome');
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