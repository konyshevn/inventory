<template>
  <div class="doc-income-item container">


    <br>
    <br>

    <table class="table table-bordered table_unit">
      <thead>
        <tr>
          <th width="40%">Устройство</th>
          <th width="30%">Сотрудник</th>
          <th width="10%">Количество</th>
          <th width="20%">Комментарий</th>
        </tr>
      </thead>
      <tbody>
      <tr v-for="rec in doc['docincome'].table_unit" :key="rec.id">
        <td>
          <catlg-widget widget-type="device" :model.sync="rec['device']"></catlg-widget>
        </td>
        <td>
          <catlg-widget widget-type="person" :model.sync="rec['person']"></catlg-widget>
        </td>
        <td>{{rec.qty}}</td>
        <td>{{rec.comment}}</td>
      </tr>
      </tbody>
    </table>
    <catlg-widget-modal></catlg-widget-modal>
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
import CatlgWidget from './CatlgWidget.vue';
import CatlgWidgetModal from './CatlgWidgetModal.vue';


Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('MM.DD.YYYY hh:mm:ss')
  }
})


export default {
  name: 'DocIncomeItem',
  components: {
    CoolSelect,
    CatlgWidget,
    CatlgWidgetModal,

  },
  props: {
    //msg: String
  },
  
  mixins: [CatlgCommon, DocCommon],
  
  data () {
    return {
      active: false
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
    this.getDocItem('docincome', 234);
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

