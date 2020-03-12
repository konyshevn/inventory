<template>
  <div class="doc-income-list container">
    <vue-headful :title="docTitle(status.docType, 'plural')"/>
    <header>
      <h2>{{docTitle(status.docType, 'plural')}}</h2>
    </header>
    <b-container class="text-left control-panel">
      <doc-list-control-panel :status.sync="status"></doc-list-control-panel>
    </b-container>

     <smart-table 
      :table-padd="200"
      :selected-plural="true"
      :selectAll="true"
      :selected.sync="status.selected"
      :dblclick-row="DocClickRow"
      :sort-by.sync="status.sortBy"
      :sort-asc.sync="status.sortAsc"
      :items="GETdocs(status.docType)"
      :fields="[
        {key: 'doc_date', label: 'Дата', type: 'text', width: '15%',
        formatter: (value) => {return formatDate(value)},
        formatterSort: false,
        },
        {key: 'doc_num', label: 'Номер', type: 'text', width: '10%',
        },
        {key: 'active', label: 'Проведен', type: 'boolean', width: '10%',},
        {key: 'department', label: 'Подразделение', type: 'text', width: '25%',
        formatter: (value, key) => {return GETcatlgItemLabel(key, value)}
        },
        {key: 'stock', label: 'Склад', type: 'text', width: '15%',
        formatter: (value, key) => {return GETcatlgItemLabel(key, value)}
        },
        {key: 'comment', label: ' Комментарий', type: 'text', width: '20%',},
      ]"
    >
      
    </smart-table>
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
import SmartTable from '@/components/common/SmartTable.vue'

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('DD.MM.YYYY HH:mm:ss')
  }
})


export default {
  name: 'DocIncomeList',
  components: {
    DocListControlPanel,
    SmartTable,
  },

  mixins:[DocCommon],
  
  props: {
  },
  
  data () {
    return {
      status: {
        selected: [],
        docType: 'docincome',
        sortBy: 'doc_date',
        sortAsc: false,
      },
    }
  },
  computed: {
    ...mapGetters([
      'GETdocs',
      'GETcatlgItemLabel',
    ])
  },

  methods: {

    ...mapActions([
      'FETCHdocs',
    ]),
    ...mapMutations([
      'UPDdocsSelected',
    ]),


  },

  async mounted () {
    const vm = this
    await this.FETCHdocs([vm.status.docType]);
    // console.log('mounted: GETdocs', vm.GETdocs(vm.status.docType))
    document.addEventListener('mousedown', function (event) {
      if (event.detail > 1) {
        event.preventDefault();
      }
    }, false);
  },
  
  created() {

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