<template>
  <div class="container">
    <vue-headful title="Отчет: Местоположение на дату"/>
    <header>
      <h2 class="align-middle">Местоположение на дату </h2>
      <b-button 
      variant="success" 
      style="margin-left: 20px;"
      @click="buildReport()">
        Сформировать
      </b-button>
      <b-button v-b-toggle.report-settings class="m-1">Настройки</b-button>
    </header>

    <b-collapse id="report-settings" v-model="showSettings">
      <report-control-panel :status.sync="status"> </report-control-panel>
    </b-collapse>

    <div v-if="loading" class="loading-spinner" >
      <b-spinner ></b-spinner>   
      <br><br>
      <strong>Загрузка...</strong>
    </div>

    <smart-table 
    v-if="!loading"
    disable-select
    :table-padd="200"
    :sort-by.sync="status.sortBy"
    :sort-asc.sync="status.sortAsc"
    :items="reportData"
    :fields="[
      {key: 'device', label: 'Устройство', type: 'text', width: '40%',
      formatter: (value, key) => {return GETcatlgItemLabel(key, value)}
      },
      {key: 'department', label: 'Подразделение', type: 'text', width: '25%',
      formatter: (value, key) => {return GETcatlgItemLabel(key, value)}
      },
      {key: 'stock', label: 'Склад', type: 'text', width: '10%',
      formatter: (value, key) => {return GETcatlgItemLabel(key, value)}
      },
      {key: 'person', label: 'Сотрудник', type: 'text', width: '15%',
      formatter: (value, key) => {return GETcatlgItemLabel(key, value)}
      },
      {key: 'qty', label: 'Количество', type: 'number', width: '10%',
      },
    ]">
    </smart-table>
  </div>
</template>


<script>
/* eslint-disable no-console */
// import { mapGetters } from 'vuex';
// import { mapActions } from 'vuex';
// import { mapMutations } from 'vuex';
// import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
// import DocCommon from '@/components/Doc/common/DocCommon.vue';
// import CatlgWidget from '@/components/Catlg/common/Widget/CatlgWidget.vue';
import SmartTable from '@/components/common/SmartTable.vue'
// import DatetimeWidget from '@/components/Catlg/common/Widget/DatetimeWidget.vue';
import ReportControlPanel from '@/components/Report/common/ReportControlPanel.vue';
import ReportCommon from '@/components/Report/common/ReportCommon.vue';


export default {
  name: 'RepCurrentLocation',
  components: {
    // CatlgWidget,
    // DatetimeWidget,
    SmartTable,
    ReportControlPanel,
  },

  mixins: [ReportCommon],
  
  props: {
  },
    
  data () {
    return {
      status: {
        reportName: 'RepCurrentLocation',
        filterReq: {
          // device: null,
          // date_to: null,
          // person: null,
          // stock: null,
        },
        fieldsOptions: {},
        filterOptions: {},
        sortBy: 'device',
        sortAsc: true,
      },
      showSettings: true,
      reportData: null,
      loading: false,
    }       
  },

  methods: {
  },

  computed: {
  },

  created: function() {
  }, 

  beforeDestroy: function() {
  },

}
   

</script>


<style>

</style>

