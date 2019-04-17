<template>
  <div class="doc-income-item container">
    <br>
    <br>

    <table class="table table-bordered table_unit">
      <thead>
        <tr>
          <th>Устройство</th>
          <th>Сотрудник</th>
          <th>Количество</th>
          <th>Комментарий</th>
        </tr>
      </thead>
      <tbody>
      <tr v-for="rec in doc['docincome'].table_unit" :key="rec.id">
        <td>
          <div style="position:relative;display:block">
          <cool-select 
          v-model="rec['device']" 
          :items="catlgs['device']"
          item-value="id"
          item-text="label"
          arrowsDisableInstantSelection="true"
          scrollItemsLimit="10"
          >
            <template slot="no-data">
              <span>Не найдено</span>
            </template>
            <template slot="item" slot-scope="{ item }">
              <div class="item">
                <span class="item-name"> {{ item.label }} </span>
              </div>
            </template>
          </cool-select>
          </div>
        </td>
        <td>
          <div style="position:relative;display:block">
          <cool-select 
          v-model="rec['person']" 
          :items="catlgs['person']"
          item-value="id"
          item-text="label"
          arrowsDisableInstantSelection="true"
          scrollItemsLimit="10">
          </cool-select>
            
          </div>
        </td>
        <td>{{rec.qty}}</td>
        <td>{{rec.comment}}</td>
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
import { CoolSelect } from 'vue-cool-select'


Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('MM.DD.YYYY hh:mm:ss')
  }
})


export default {
  name: 'DocIncomeItem',
  components: {
    CoolSelect
  },
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
    },

    getLabel (item) {
      return item.label
    },
     
  },

  computed: {

  },
  
  mounted: function () {
    this.getDocItem('docincome', 225);
  },

  created: function() {
  }, 

}
   



</script>

<style scoped>
tbody tr:hover {
background-color: #f2f2f2;
color: #000000
}

</style>

