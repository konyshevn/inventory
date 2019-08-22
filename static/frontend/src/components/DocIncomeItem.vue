<template>
  <div class="doc-income-item container">
    <div class="sticky1 container" style1="position: fixed; background: white; z-index: 10;">
    <header>
      <h2 align="left">Оприходование</h2>
      <b-badge v-if="true" variant="info">редактируется</b-badge> 
    </header>
      <b-container class="text-left" >
        <doc-item-control-panel :doc="currentDoc"></doc-item-control-panel>
        <p></p>

        <b-row align-v="end" class="mb-2">
          <b-col sm="1"> 
            <label>Номер:</label> 
          </b-col>
          <b-col sm="2">
            <b-form-input v-model="doc_num" type="number" number></b-form-input>
          </b-col>
          <b-col sm="1">
            <label>Дата:</label> 
          </b-col>
          <b-col sm="3">
            <datetime-widget v-if="doc_date" :model.sync="doc_date"></datetime-widget>
          </b-col>
          <b-col sm="2" align="center">
            <b-button v-if="active" disabled variant="success">Проведен</b-button>
            <b-button v-if="!active" disabled variant="light">Не проведен</b-button>
          </b-col>
        </b-row>

        <b-row align-v="end" class="mb-2">
          <b-col sm="2" align-h="start">
            <label>Подразделение:</label>
          </b-col> 
          <b-col sm="5">
            <catlg-widget widget-type="department" required :model.sync="department"></catlg-widget>
            
          </b-col> 
        </b-row>

        <b-row align-v="end" class="mb-2">
          <b-col sm="2" align-h="start">
            <label>Склад:</label>
          </b-col> 
          <b-col sm="5">
            <catlg-widget widget-type="stock" :model.sync="stock"></catlg-widget>
          </b-col> 
        </b-row>

        <b-row align-v="end" class="mb-2">
          <b-col sm="2" align-h="start">
            <label>Комментарий:</label>
          </b-col>
          <b-col sm="8" align-h="start"> 
            <b-form-input v-model="comment" type="text" maxlength="70"></b-form-input>
          </b-col>
        </b-row>
      </b-container>
      <b-container class="text-left" >
        <table-unit-control-panel></table-unit-control-panel>
      </b-container>
    </div>

    <div >
      <table class="table table-bordered table_unit">
        <thead >
          <tr >
            <th>У</th>
            <table-unit-header sort-type="widget" sort-field="device">Устройство</table-unit-header>
            <table-unit-header sort-type="widget" sort-field="person">Сотрудник</table-unit-header>
            <table-unit-header sort-type="number" sort-field="qty">Количество</table-unit-header>
            <table-unit-header sort-type="text" sort-field="comment">Комментарий</table-unit-header>
          </tr>
        </thead>
        <tbody>
          <table-unit-item v-for="(rec, index) in currentDoc.table_unit" :index="index">
          </table-unit-item>
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
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';
import TableUnitItem from './TableUnitItem.vue';
import TableUnitHeader from './TableUnitHeader.vue';

function mapTwoWay (key, getter, mutation) {
  return {
    get () {
      return this.$store.getters[getter][key]
    },
    set (value) {
      this.$store.commit(mutation, [key, value])
    }
  }
}

function mapTwoWayTU (key, getter, mutation) {
  return {
    get () {
      return this.$store.getters[getter][key]
    },
    set (value) {
      console.log(value)
      this.$store.commit(mutation, [key, value])
    }
  }
}

export default {
  name: 'DocIncomeItem',
  components: {
    CatlgWidget,
    CatlgWidgetModal,
    DatetimeWidget,
    DocItemControlPanel,
    TableUnitControlPanel,
    TableUnitItem,
    TableUnitHeader,

  },
  props: {
    id: Number,
  },
  
  mixins: [CatlgCommon, DocCommon],
  
  data () {
    return {
      docChanged: false,
    }       
  },

  methods: {
    ...mapMutations([
      'UPDcurrentDoc',
      'UPDcurrentDocTU',
      'DELcurrentDoc',
      'sortTU',
      'INITcurrentDoc',
    ]),

    ...mapActions([
      'FETCHcurrentDoc'
    ])
  },

  computed: {
    doc_num: mapTwoWay('doc_num', 'currentDoc', 'UPDcurrentDoc'),
    doc_date: mapTwoWay('doc_date', 'currentDoc', 'UPDcurrentDoc'),
    department: mapTwoWay('department', 'currentDoc', 'UPDcurrentDoc'),
    stock: mapTwoWay('stock', 'currentDoc', 'UPDcurrentDoc'),
    comment: mapTwoWay('comment', 'currentDoc', 'UPDcurrentDoc'),
    active: mapTwoWay('active', 'currentDoc', 'UPDcurrentDoc'),

    ...mapGetters([
      'currentDoc',
      'currentDocTU',

    ])
  },

 
  mounted: function () {
    var vm = this
    //this.$nextTick(function () {
    //  vm.getDocItem('docincome', vm.id);
    //})
    if (vm.id == "new") {
      vm.DELcurrentDoc()
      vm.INITcurrentDoc('docincome')
    } else {
      vm.FETCHcurrentDoc(['docincome', vm.id])
    }
  },

  created: function() {
  }, 

  beforeDestroy: function() {
    console.log('beforeDestroy')
    this.DELcurrentDoc()
  },

}
   



</script>

<style >
.table_unit tbody tr:hover {
    background-color: #f2f2f2;
    color: #000000
  }

.table_unit td, .table_unit th {
  padding: 0.30rem !important;
}


.table_unit td:nth-child(1), .table_unit th:nth-child(1) {
  width: 5%;
}
.table_unit td:nth-child(2), .table_unit th:nth-child(2) {
  width: 35%;
}
.table_unit td:nth-child(3), .table_unit th:nth-child(3) {
  width: 25%;
}
.table_unit td:nth-child(4), .table_unit th:nth-child(4) {
  width: 15%;
}
.table_unit td:nth-child(5), .table_unit th:nth-child(5) {
  width: 20%;
}

.table_unit {
  display: inline-grid;
  grid-template-areas: 
  "head-fixed" 
  "body-scrollable";
}

.table_unit thead {
  grid-area: head-fixed;
  /* fallback */
  width: 100%;
  /* minus scroll bar width */
  width: calc( 100% - 1em ) !important;/* scrollbar is average 1em/16px width, remove it from thead width */
  cursor: pointer;
}

.table_unit tbody {
  grid-area: body-scrollable;
  overflow-y: scroll;
  height: calc(90vh  - 350px);
}


.table_unit thead, .table_unit tbody tr {
    display:table;
    table-layout:fixed;/* even columns width , fix width of table too*/
}

.select-row {
  vertical-align: middle; 
  text-align: center;
}

header { text-align: left; }
header > h2 { display: inline-block; }
header span { margin-left: 10px;}


</style>

