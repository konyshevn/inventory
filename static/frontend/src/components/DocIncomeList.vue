<template>
  <div class="doc-income-list container">
    <h1 align="left">Оприходования</h1>
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
      <tr v-for="doc in GETdocs" :key="doc.id" @dblclick="clickRow(doc.id, $event)" >
        <td>{{doc.doc_date | formatDate}}</td>
        <td>{{doc.doc_num}}</td>
        <td>
          <span v-if="doc.active">Да</span>
          <span v-else></span>
        </td>
        <td><span>{{GETcatlgItemLabel('department', doc.department)}}</span></td>
        <td><span>{{GETcatlgItemLabel('stock', doc.stock)}}</span></td>
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
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';

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
 // mixins: [CatlgCommon, DocCommon],
  data () {
    return {
    }
  },
  methods: {

    clickRow: function (id, event) {
      console.log(id);
      this.$router.push({ name: 'doc.item', params: {id: id, docType: 'docincome'} })
    },
     
    ...mapActions([
      'FETCHdocs',
    ])
  },
  mounted: function () {
    this.FETCHdocs('docincome');
    
    document.addEventListener('mousedown', function (event) {
      if (event.detail > 1) {
        event.preventDefault();
      }
    }, false);
  },
  
  created() {
    //this.fetchDocs('docincome');

  },

  computed: {
    ...mapGetters([
      'GETdocs',
      'GETcatlgItemLabel',
    ])
  },
}


</script>

<style scoped>
tbody tr:hover {
background-color: #f2f2f2;
color: #000000
}
</style>