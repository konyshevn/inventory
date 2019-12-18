<template>
  <div class="container">
    <header>
      <h2>{{docTitle(status.docType, 'plural')}}</h2>
    </header>
    <b-container class="text-left control-panel">
      <doc-list-control-panel :status.sync="status" ></doc-list-control-panel>
    </b-container>

     <smart-table 
      :table-padd="200"
      :min-width="1100"
      :max-width="1500"
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
        {key: 'doc_num', label: 'Номер', type: 'text', width: '6%',
        },
        {key: 'active', label: 'Проведен', type: 'boolean', width: '10%',},
        {key: 'department_from', label: 'Подразделение отправитель', type: 'text', width: '15%',
        formatter: (value, key) => {return GETcatlgItemLabel('department', value)}
        },
        {key: 'department_to', label: 'Подразделение получатель', type: 'text', width: '15%',
        formatter: (value, key) => {return GETcatlgItemLabel('department', value)}
        },
        {key: 'stock_from', label: 'Склад отправитель', type: 'text', width: '12%',
        formatter: (value, key) => {return GETcatlgItemLabel('stock', value)}
        },
        {key: 'stock_to', label: 'Склад получатель', type: 'text', width: '12%',
        formatter: (value, key) => {return GETcatlgItemLabel('stock', value)}
        },
        {key: 'comment', label: ' Комментарий', type: 'text', width: '10%',},
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
  name: 'DocMoveList',
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
        docType: 'docmove',
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
    await this.FETCHdocs(vm.status.docType);
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
.container {
  max-width: 1300px !important;
}

</style>