<template>
  <div class="doc-income-list container">
    <header>
      <h2>{{docTitle(status.docType, 'plural')}}</h2>
    </header>
    <b-container class="text-left">
      <doc-list-control-panel :status="status"></doc-list-control-panel>
    </b-container>
    <table class="table table-bordered doc-list" id="doc-list">
      <thead>
        <tr>
          <th @click="selectAllRows(GETdocs)"><font-awesome-icon icon="check-square"/></th>
          <sort-header obj-type="docs" field-type="text" sort-field="doc_date">Дата</sort-header>
          <sort-header obj-type="docs" field-type="text" sort-field="doc_num">Номер</sort-header>
          <sort-header obj-type="docs" field-type="text" sort-field="active">Проведен</sort-header>
          <sort-header obj-type="docs" field-type="widget" sort-field="department">Подразделение</sort-header>
          <sort-header obj-type="docs" field-type="widget" sort-field="stock">Склад</sort-header>
          <sort-header obj-type="docs" field-type="text" sort-field="comment">Комментарий</sort-header>
        </tr>
      </thead>
      <tbody>
      <tr v-for="doc in GETdocs" :key="doc.id" 
      @dblclick="clickRow(doc.id, $event)" 
      @click="selectRow(doc.id, $event)"
      :class="{'row-selected': isRowSelected(doc.id)}">
        <td>
          <b-form-checkbox
          v-model="status.selected"
          :value="doc.id"
          button-variant="danger"
          >
          </b-form-checkbox>
        </td>
        <td>{{doc.doc_date | formatDate}}</td>
        <td>{{doc.doc_num}}</td>
        <td>
          <span v-if="doc.active"><font-awesome-icon icon="check"/></span>
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
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';
import moment from 'moment';
import DocCommon from '@/components/Doc/common/DocCommon.vue';
import DocListControlPanel from '@/components/Doc/common/ControlPanel/DocListControlPanel.vue'
import SortHeader from '@/components/common/SortHeader.vue'

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('DD.MM.YYYY HH:mm:ss')
  }
})


export default {
  name: 'DocIncomeList',
  components: {
    DocListControlPanel,
    SortHeader,
  },
  mixins:[DocCommon],
  props: {
  },
  data () {
    return {
      status: {
        selected: [],
        docType: 'docincome',
      },
    }
  },
  methods: {

    ...mapActions([
      'FETCHdocs',
    ]),
    ...mapMutations([
      'UPDdocsSelected',
    ]),


  },

  mounted: function () {
    const vm = this
    this.FETCHdocs(vm.status.docType);
    
    document.addEventListener('mousedown', function (event) {
      if (event.detail > 1) {
        event.preventDefault();
      }
    }, false);
  },
  
  created() {

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
.doc-list tbody{
  display:block;
  overflow:auto;
  min-width: 1100px;
  height: calc(100vh  - 200px);
}

.doc-list thead tr{
  display:block;
  width: calc( 100% - 1em ) !important;
  cursor: pointer;
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