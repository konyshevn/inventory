<template>
  <div class="doc-income-item container">

<!--
    <v-app>
    <v-autocomplete 
      :items="[{'text': 'test1'}, {'text': 'qwe'}]"
      v-model="model"
      persistent-hint>
    </v-autocomplete>
    </v-app> 
-->
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
      <tr v-for="rec in doc['docincome'].table_unit" :key="rec.id">
        <td>{{getCatlgLabel('device', rec.device)}}</td>
        <td>{{getCatlgLabel('person', rec.person)}}</td>
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
  
  mixins: [CatlgCommon, DocCommon],
  
  data () {
    return {
    }
  },

  methods: {
    
    clickRow: function (id) {
      console.log(id);
    },

     
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