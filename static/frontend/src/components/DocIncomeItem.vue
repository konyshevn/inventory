<template>
  <div class="doc-income-item container">

    <h1 align="left">Оприходование</h1>
      <b-container class="text-left" >
        <b-row align-v="end" class="mb-2">
          <b-col sm="1"> 
            <label :for="doc_num">Номер:</label> 
          </b-col>
          <b-col sm="2">
            <b-form-input :id="doc_num" v-model="doc['docincome'].doc_num" type="number"></b-form-input>
          </b-col>
          <b-col sm="1">
            <label :for="doc_date">Дата:</label> 
          </b-col>
          <b-col sm="3">
            <datetime-widget v-if="doc['docincome'].doc_date" :model.sync="doc['docincome'].doc_date"></datetime-widget>
          </b-col>
        </b-row>

        <b-row align-v="end" class="mb-2">
          <b-col sm="2" align-h="start">
            <label>Подразделение:</label>
          </b-col> 
          <b-col sm="5">
            <catlg-widget widget-type="department" :init-item="catlgs" :model.sync="doc['docincome'].department"></catlg-widget>
          </b-col> 
        </b-row>

        <b-row align-v="end" class="mb-2">
          <b-col sm="2" align-h="start">
            <label>Склад:</label>
          </b-col> 
          <b-col sm="5">
            <catlg-widget widget-type="stock" :init-item="catlgs" :model.sync="doc['docincome'].stock"></catlg-widget>
          </b-col> 
        </b-row>

        <b-row align-v="end" class="mb-2">
          <b-col sm="2" align-h="start">
            <label>Комментарий:</label>
          </b-col>
          <b-col sm="8" align-h="start"> 
            <b-form-input v-model="doc['docincome'].comment" type="string" maxlength="70"></b-form-input>
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
import CatlgWidget from './CatlgWidget.vue';
import DatetimeWidget from './DatetimeWidget.vue';
import CatlgWidgetModal from './CatlgWidgetModal.vue';


export default {
  name: 'DocIncomeItem',
  components: {
    CatlgWidget,
    CatlgWidgetModal,
    DatetimeWidget,

  },
  props: {
    id: Number
  },
  
  mixins: [CatlgCommon, DocCommon],
  
  data () {
    return {
    }       
  },

  methods: {
  },

  computed: {
  },
  
  mounted: function () {
    var vm = this
    //this.$nextTick(function () {
      vm.getDocItem('docincome', vm.id);
    //})
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

  .static {
    position: sticky;
    top: 0;

  }

</style>

