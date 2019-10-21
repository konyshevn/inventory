<template>
  <div class="doc-income-list container">
    <h2 align="left">Оприходование</h2>
    <b-container class="text-left">
      <doc-list-control-panel :status="status"></doc-list-control-panel>
    </b-container>
    <table class="table table-bordered doc-list" id="doc-list">
      <thead>
        <tr>
          <th>У</th>
          <sort-header obj-type="docs" field-type="text" sort-field="doc_date">Дата</sort-header>
          <sort-header obj-type="docs" field-type="text" sort-field="doc_num">Номер</sort-header>
          <sort-header obj-type="docs" field-type="text" sort-field="active">Проведен</sort-header>
          <sort-header obj-type="docs" field-type="widget" sort-field="department">Подразделение</sort-header>
          <sort-header obj-type="docs" field-type="widget" sort-field="stock">Склад</sort-header>
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
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';
import moment from 'moment';
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
import DocCommon from '@/components/Doc/common/DocCommon.vue';
import DocListControlPanel from '@/components/Doc/common/ControlPanel/DocListControlPanel.vue'
import SortHeader from '@/components/common/SortHeader.vue'

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
  },
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

.doc-list tbody tr:hover {
background-color: #f2f2f2;
color: #000000
}


.doc-list th, .doc-list td {
padding: 0.25rem !important;
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