<template>
  <div class="doc-income-item container">
    <div class="sticky">
    <h2 align="left">Оприходование</h2>
    <b-form @submit.prevent>
      <b-container class="text-left" >
        <doc-item-control-panel :doc="doc"></doc-item-control-panel>
        <p></p>

        <b-row align-v="end" class="mb-2">
          <b-col sm="1"> 
            <label :for="doc_num">Номер:</label> 
          </b-col>
          <b-col sm="2">
            <b-form-input :id="doc_num" v-model="doc.doc_num" type="number"></b-form-input>
          </b-col>
          <b-col sm="1">
            <label :for="doc_date">Дата:</label> 
          </b-col>
          <b-col sm="3">
            <datetime-widget v-if="doc.doc_date" :model.sync="doc.doc_date"></datetime-widget>
          </b-col>
          <b-col sm="1" align="center">
            <b-button v-if="doc.active" disabled variant="success">Проведен</b-button>
            <b-button v-if="!doc.active" disabled variant="light">Не проведен</b-button>
          </b-col>
        </b-row>

        <b-row align-v="end" class="mb-2">
          <b-col sm="2" align-h="start">
            <label>Подразделение:</label>
          </b-col> 
          <b-col sm="5">
            <catlg-widget widget-type="department" required :init-item="catlgs" :model.sync="doc.department"></catlg-widget>
          </b-col> 
        </b-row>

        <b-row align-v="end" class="mb-2">
          <b-col sm="2" align-h="start">
            <label>Склад:</label>
          </b-col> 
          <b-col sm="5">
            <catlg-widget widget-type="stock" :init-item="catlgs" :model.sync="doc.stock"></catlg-widget>
          </b-col> 
        </b-row>

        <b-row align-v="end" class="mb-2">
          <b-col sm="2" align-h="start">
            <label>Комментарий:</label>
          </b-col>
          <b-col sm="8" align-h="start"> 
            <b-form-input v-model="doc.comment" type="string" maxlength="70"></b-form-input>
          </b-col>
        </b-row>
      </b-container>
    </b-form>
    </div>

    <div>
      <b-container class="text-left" >
        <table-unit-control-panel :doc="doc"></table-unit-control-panel>
      </b-container>
      <table class=" fixed_header table table-bordered table_unit ">
        <thead>
          <tr>
            <th width="40%">Устройство</th>
            <th width="30%">Сотрудник</th>
            <th width="10%">Количество</th>
            <th width="20%">Комментарий</th>
          </tr>
        </thead>
        <tbody>
        <tr v-for="rec in doc.table_unit" :key="rec.id">
          <td>
            <catlg-widget widget-type="device" required :init-item="catlgs" :model.sync="rec['device']"></catlg-widget>
          </td>
          <td>
            <catlg-widget widget-type="person" required :init-item="catlgs" :model.sync="rec['person']"></catlg-widget>
          </td>
          <td><b-form-input :id="qty" v-model="rec.qty" type="number"></b-form-input></td>
          <td><b-form-input :id="comment" v-model="rec.comment" type="string"></b-form-input></td>
        </tr>
        </tbody>
      </table>
  </div>

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
import DocItemControlPanel from './DocItemControlPanel.vue';
import TableUnitControlPanel from './TableUnitControlPanel.vue';


export default {
  name: 'DocIncomeItem',
  components: {
    CatlgWidget,
    CatlgWidgetModal,
    DatetimeWidget,
    DocItemControlPanel,
    TableUnitControlPanel,

  },
  props: {
    id: Number,
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
.table_unit tbody tr:hover {
    background-color: #f2f2f2;
    color: #000000
  }

  .sticky {
    position: sticky;
    top: 0;
    min-height: 3em;
    top: 3em;
    background: white;
    z-index: 1;
  }

.table_unit td, .table_unit th {
  padding: 0.30rem !important;
}
</style>

