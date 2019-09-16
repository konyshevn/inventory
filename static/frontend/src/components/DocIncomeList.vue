<template>
  <div class="doc-income-list container">
    <h2 align="left">Оприходование</h2>
    <b-container class="text-left">
      <doc-list-control-panel :status="status"></doc-list-control-panel>
    </b-container>
    <table class="table table-bordered doc-list">
      <thead>
        <tr>
          <th>У</th>
          <sort-header obj-type="docs" field-type="text" sort-field="doc_date">Дата</sort-header>
          <sort-header obj-type="docs" field-type="text" sort-field="doc_num">Номер</sort-header>
          <sort-header obj-type="docs" field-type="text" sort-field="active">Проведен</sort-header>
          <sort-header obj-type="docs" field-type="text" sort-field="department">Подразделение</sort-header>
          <sort-header obj-type="docs" field-type="text" sort-field="stock">Склад</sort-header>
          <sort-header obj-type="docs" field-type="text" sort-field="comment">Комментарий</sort-header>
        </tr>
      </thead>
      <tbody>
      <tr v-for="doc in GETdocs" :key="doc.id" @dblclick="clickRow(doc.id, $event)" >
        <td>
          <b-form-checkbox
          v-model="status.selected"
          :value="doc.id"
          >
          </b-form-checkbox>
        </td>
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
import { mapMutations } from 'vuex';
import DocListControlPanel from './DocListControlPanel.vue'
import SortHeader from './SortHeader.vue'

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('DD.MM.YYYY hh:mm:ss')
  }
})


export default {
  name: 'DocIncomeList',
  components: {
    DocListControlPanel,
    SortHeader,
  },
  props: {
    //msg: String
  },
 // mixins: [CatlgCommon, DocCommon],
  data () {
    return {
      status: {
        selected: [],
      },
    }
  },
  methods: {

    clickRow: function (id, event) {
      console.log(id);
      this.$router.push({ name: 'doc.item', params: {id: id, docType: 'docincome'} })
    },
     
    ...mapActions([
      'FETCHdocs',
    ]),
    ...mapMutations([
      'UPDdocsSelected',
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
.doc-list tbody tr:hover {
background-color: #f2f2f2;
color: #000000
}

.doc-list {
  display: inline-grid;
  grid-template-areas: 
  "head-fixed" 
  "body-scrollable";
}

.doc-list thead {
  grid-area: head-fixed;
  /* fallback */
  width: 100%;
  /* minus scroll bar width */
  width: calc( 100% - 1em ) !important;/* scrollbar is average 1em/16px width, remove it from thead width */
  cursor: pointer;
}

.doc-list tbody {
  grid-area: body-scrollable;
  overflow-y: scroll;
  height: calc(90vh  - 140px);
}

.doc-list thead, .doc-list tbody tr {
    display:table;
    table-layout:fixed;/* even columns width , fix width of table too*/
}

.doc-list td:nth-child(1), .doc-list th:nth-child(1) {
  width: 5%;
}
.doc-list td:nth-child(2), .doc-list th:nth-child(2) {
  width: 14%;
}
.doc-list td:nth-child(3), .doc-list th:nth-child(3) {
  width: 10%;
}
.doc-list td:nth-child(4), .doc-list th:nth-child(4) {
  width: 8%;
}
.doc-list td:nth-child(5), .doc-list th:nth-child(5) {
  width: 20%;
}
.doc-list td:nth-child(6), .doc-list th:nth-child(6) {
  width: 15%;
}
.doc-list td:nth-child(7), .doc-list th:nth-child(7) {
  width: 15%;
}

</style>