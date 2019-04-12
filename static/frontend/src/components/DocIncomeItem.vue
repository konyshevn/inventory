<template>
  <div class="doc-income-item container">

    <selectize 
          v-model="select_model" :settings="getSelectizeSettings">
    </selectize>
    <br>

    <v-app>
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
        <td>
          <selectize 
          v-model="select_model" :settings="getSelectizeSettings">
          </selectize>
        </td>
        <td>
          <v-autocomplete 
          :items="catlgs['person']"
          item-text="label"
          item-value="id"
          v-model="rec['person']"
          :loading="false">
          </v-autocomplete>
        </td>
        <td>{{rec.qty}}</td>
        <td>{{rec.comment}}</td>
      </tr>
      </tbody>
    </table>

    </v-app> 
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
import Selectize from 'vue2-selectize';


Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('MM.DD.YYYY hh:mm:ss')
  }
})


export default {
  name: 'DocIncomeItem',
  components: {
    Selectize
  },
  props: {
    //msg: String
  },
  
  mixins: [CatlgCommon, DocCommon],
  
  data () {
    return {
      select_model: 1,
      selectize_settings: {
        create: false,
        sortField: 'label',
        valueField: 'id',
        labelField: 'label',
        searchField: ['label'],
        openOnFocus: true,
        //  closeAfterSelect: true,

        render: {
            option: function (item, escape) {
                return '<div>' + escape(item.text) + '</div>';
            }
        },

        load: function(query, callback) {
            var vm=this;
            if (!query.length) return callback();
            callback(this.catlgs['device']);
            
        },
  
    }
    }
  },

  methods: {
    
    clickRow: function (id) {
      console.log(id);
    },

     
  },

  computed: {
    getSelectizeSettings: function(){
      var vm = this;
      var settings = {
        create: false,
        sortField: 'label',
        valueField: 'id',
        labelField: 'label',
        searchField: ['label'],
        openOnFocus: true,
        //  closeAfterSelect: true,

        render: {
            option: function (item, escape) {
                return '<div>' + escape(item.label) + '</div>';
            }
        },

        load: function(query, callback) {
            if (!query.length) return callback();
            callback(vm.catlgs['device']);
        },
      }
      return settings;
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

