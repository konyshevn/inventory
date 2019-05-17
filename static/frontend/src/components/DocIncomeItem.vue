<template>
  <div class="doc-income-item container">
    <br>
    <br>

      <b-container class="bv-example-row">
        <b-row align-v="end" class="mb-2">
          <b-col sm="0"> 
            <label :for="doc_num">Номер:</label> 
          </b-col>
          <b-col sm="2">
            <b-form-input :id="doc_num" v-model="doc['docincome'].doc_num" type="number"></b-form-input>
          </b-col>
          <b-col sm="0">
            <label :for="doc_date">Дата:</label> 
          </b-col>
          <b-col sm="3">
            <datetime-widget :model.sync="doc['docincome'].doc_date"></datetime-widget>
            <date-picker v-model="doc['docincome'].doc_date" :config="dtpOptions"></date-picker>
          </b-col>
        </b-row>

        <b-row align-v="end" class="mb-2">
          <b-col sm="0" align-h="start">
            <label>Подразделение:</label>
          </b-col> 
          <b-col sm="5">
            <catlg-widget widget-type="department" :init-item="catlgs" :model.sync="doc['docincome'].department"></catlg-widget>
          </b-col> 
        </b-row>

        <b-row align-v="end" class="mb-2">
          <b-col sm="0" align-h="start">
            <label>Склад:</label>
          </b-col> 
          <b-col sm="5">
            <catlg-widget widget-type="stock" :init-item="catlgs" :model.sync="doc['docincome'].stock"></catlg-widget>
          </b-col> 
        </b-row>

      </b-container>
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
          
          <catlg-widget widget-type="device"  :init-item="catlgs" :model.sync="rec['device']"></catlg-widget>
          
        </td>
        <td>
          <catlg-widget widget-type="person" :init-item="catlgs" :model.sync="rec['person']"></catlg-widget>
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
import DatetimeWidget from './DatetimeWidget.vue';
import CatlgWidgetModal from './CatlgWidgetModal.vue';
import datePicker from 'vue-bootstrap-datetimepicker';
import 'pc-bootstrap4-datetimepicker/build/css/bootstrap-datetimepicker.css';


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
    datePicker,
    DatetimeWidget,

  },
  props: {
    //msg: String
  },
  
  mixins: [CatlgCommon, DocCommon],
  
  data () {
    return {
      active: false,
      dtpDate:"2019-05-14T15:58:30+03:00",
      dtpOptions: {
        //format: 'DD.MM.YYYY HH:mm:ss',
        useCurrent: false,
        locale: 'ru-my',
        //showClear: true,
        //showClose: true,
        extraFormats: ["YYYY-MM-DD hh:mm:ss ZZZZ"],
        //language: 'ru-RU',
      }       
    }
  },

  methods: {
    
    clickRow: function (id) {
      console.log(id);
    },

    getLabel (item) {
      return item.label
    },

    widgetInitItem (widgetType, itemId) {
      var vm = this
      var initItem = []
      if (!(vm.catlgs[widgetType][itemId] == undefined)) {
        initItem.push(vm.catlgs[widgetType][itemId])
      }
      return initItem
    }
     
  },

  computed: {

  },
  
  mounted: function () {
    var vm = this
    //this.$nextTick(function () {
      vm.getDocItem('docincome', 215);
    //})
/*
    var tu = vm.doc['docincome']['table_unit']
    console.log(vm.doc['docincome'])

    this.fetchWidgetInitCatlg(this['doc']['docincome']['table_unit'], {'device': 'device', 'person': 'person'})
*/
  },

  created: function() {
      //moment.updateLocale('en', {})
  }, 

}
   



</script>

<style scoped>
tbody tr:hover {
background-color: #f2f2f2;
color: #000000
}

</style>

