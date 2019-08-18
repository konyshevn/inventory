<template>
  <div class="doc-income-item container">
    <div class="sticky1 container" style1="position: fixed; background: white; z-index: 10;">
    <h2 align="left">Оприходование</h2>
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
        <table-unit-control-panel :doc="doc" :selected="tableUnit.selected"></table-unit-control-panel>
        </b-container>
    </div>

    <div >
      <table class="table table-bordered table_unit">
        <thead >
          <tr >
            <th>
              У
            </th>
            <th v-on:click="sortTU(doc.table_unit, 'device', 'widget')">
              Устройство
              <span class="arrow" v-if="tableUnit.sort.field == 'device'" :class="tableUnit.sort.order > 0 ? 'asc' : 'dsc'">
              </span>
            </th>
            <th v-on:click="sortTU(doc.table_unit, 'person', 'widget')">
              Сотрудник
              <span class="arrow" v-if="tableUnit.sort.field == 'person'" :class="tableUnit.sort.order > 0 ? 'asc' : 'dsc'">
              </span>
            </th>
            <th v-on:click="sortTU(doc.table_unit, 'qty', 'number')">
              Количество
              <span class="arrow" v-if="tableUnit.sort.field == 'qty'" :class="tableUnit.sort.order > 0 ? 'asc' : 'dsc'">
              </span>
            </th>
            <th v-on:click="sortTU(doc.table_unit, 'comment', 'text')">
              Комментарий
              <span class="arrow" v-if="tableUnit.sort.field == 'comment'" :class="tableUnit.sort.order > 0 ? 'asc' : 'dsc'">
              </span>
            </th>
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
    ...mapMutations([
      'UPDcurrentDoc',
      'UPDcurrentDocTU',
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

    ...mapGetters([
      'currentDoc',
      'currentDocTU',
    ])
  },
  
  mounted: function () {
    //var vm = this
    //this.$nextTick(function () {
    //  vm.getDocItem('docincome', vm.id);
    //})
    this.FETCHcurrentDoc(['docincome', this.id])
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

.table_unit td, .table_unit th {
  padding: 0.30rem !important;
}


.table_unit td:nth-child(1), th:nth-child(1) {
  width: 5%;
}
.table_unit td:nth-child(2), th:nth-child(2) {
  width: 35%;
}
.table_unit td:nth-child(3), th:nth-child(3) {
  width: 25%;
}
.table_unit td:nth-child(4), th:nth-child(4) {
  width: 15%;
}
.table_unit td:nth-child(5), th:nth-child(5) {
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
  overflow: auto;
  height: calc(90vh  - 350px);
}


.table_unit thead, tbody tr {
    display:table;
    table-layout:fixed;/* even columns width , fix width of table too*/
}

.arrow {
  display: inline-block;
  vertical-align: middle;
  width: 0;
  height: 0;
  margin-left: 5px;
  opacity: 0.66;
}

.arrow.asc {
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-bottom: 6px solid black;
}

.arrow.dsc {
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-top: 6px solid black;
}

.select-row {
  vertical-align: middle; 
  text-align: center;
}
</style>

